# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


import os
import struct
from twisted.internet import threads, reactor
from enigma import ePicLoad, gPixmapPtr, ePoint, eSize
from Components.AVSwitch import AVSwitch
from Tools.BoundFunction import boundFunction
from .Debug import logger
from .WebRequests import WebRequests


PNG_SIGNATURE = bytes([0x89]) + b"PNG" + bytes([0x0D, 0x0A, 0x1A, 0x0A])
JPEG_SOI = bytes([0xFF, 0xD8])
JPEG_NO_SIZE_MARKERS = (0xC4, 0xC8, 0xCC)  # inside the SOF range, but not frame headers


def getImageSize(path):
    """(width, height) of a JPEG or PNG file read from its header, or None - ePicLoad only reports the size
    of a picture after decoding it, and by then it has padded it to the box it was asked for."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
            if head.startswith(PNG_SIGNATURE):
                return struct.unpack(">II", head[16:24])
            if not head.startswith(JPEG_SOI):
                return None
            f.seek(2)
            while True:
                byte = f.read(1)
                if not byte:
                    return None
                if byte[0] != 0xFF:
                    continue
                marker = f.read(1)
                while marker and marker[0] == 0xFF:  # fill bytes
                    marker = f.read(1)
                if not marker:
                    return None
                code = marker[0]
                if code == 0x01 or 0xD0 <= code <= 0xD8 or code == 0x00:  # no length field
                    continue
                length = struct.unpack(">H", f.read(2))[0]
                if 0xC0 <= code <= 0xCF and code not in JPEG_NO_SIZE_MARKERS:
                    _precision, height, width = struct.unpack(">BHH", f.read(5))
                    return width, height
                f.seek(length - 2, 1)
    except (OSError, struct.error):
        return None


MAX_PICTURE_WIDTH = 1280  # wider pictures are reduced to this when they are downloaded


def shrinkPicture(path, max_width=MAX_PICTURE_WIDTH):
    """Reduce a downloaded picture in place to at most max_width pixels wide. The originals of some channels are 5000x3300
    pixels (4 MB), which the box needs a second or more to decode: the posters of the columns then appear one by one, as if
    they were fetched from the internet. Left alone when it is small enough or PIL is not installed."""
    try:
        from PIL import Image
    except ImportError:
        return
    temp_path = path + ".tmp"
    try:
        with Image.open(path) as img:
            if img.width <= max_width:
                return
            height = max(1, round(img.height * max_width / img.width))
            img.draft("RGB", (max_width, height))  # the JPEG decoder scales by 1/2, 1/4 or 1/8 while it decodes: fast, little memory
            resample = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
            small = img.convert("RGB").resize((max_width, height), resample)
            small.save(temp_path, "JPEG", quality=85)
        os.replace(temp_path, path)
        logger.debug("shrunk to %sx%s: %s", max_width, height, path)
    except Exception as e:
        logger.error("path: %s, exception: %s", path, e)
        try:
            os.remove(temp_path)
        except OSError:
            pass


class Picture(WebRequests):
    def __init__(self, temp_dir):
        WebRequests.__init__(self)
        self.temp_dir = temp_dir
        self.sc = AVSwitch().getFramebufferScale()
        self.picload_cache = {}
        self.picload_conn_cache = {}
        self.pixmap_boxes = {}

    def showPicture(self, pixmap, atype, ident, url):
        logger.info("atype: %s, ident: %s, url: %s", atype, ident, url)
        path = os.path.join(self.temp_dir, atype + str(ident) + ".jpg")
        if url and not url.endswith("None") and not os.path.isfile(path):
            threads.deferToThread(self.downloadPicture,
                                  pixmap, url, path, self.displayPicture)
        else:
            self.displayPicture(pixmap, path)

    def downloadPicture(self, pixmap, url, path, callback):
        logger.info("path: %s", path)
        self.downloadFile(url, path)
        shrinkPicture(path)
        logger.debug("downloaded: %s", path)
        reactor.callFromThread(callback, pixmap, path)

    def displayPicture(self, pixmap, path):
        logger.info("path: %s", path)
        if os.path.isfile(path):
            if path not in self.picload_cache:
                self.picload_cache[path] = ePicLoad()
            picload = self.picload_cache[path]
            if path not in self.picload_conn_cache:
                picload.PictureData.get().append(boundFunction(self.onPictureReady, path, pixmap))
                self.picload_conn_cache[path] = True
            _x, _y, box_w, box_h = self.getBox(pixmap)
            # decode at the size the picture will really have in the box (aspect ratio kept) - ePicLoad would
            # otherwise pad it to the whole box with background color, which hides rounded corners
            image_size = getImageSize(path)
            if image_size and image_size[0] > 0 and image_size[1] > 0:
                factor = min(box_w / image_size[0], box_h / image_size[1])
                box_w = max(1, int(image_size[0] * factor))
                box_h = max(1, int(image_size[1] * factor))
            picload.setPara(
                (
                    box_w,
                    box_h,
                    self.sc[0], self.sc[1],
                    False,
                    1,
                    "#00000000"
                )
            )
            picload.startDecode(path)  # Asynchronous call
        else:
            logger.error("pixmap not found: %s", path)
            pixmap.instance.setPixmap(gPixmapPtr())

    def getBox(self, pixmap):
        """The area the skin gave the widget (x, y, width, height). Remembered on first use, because
        fitWidget() resizes the widget itself and the box has to stay the skin's."""
        if pixmap not in self.pixmap_boxes:
            instance = pixmap.instance
            self.pixmap_boxes[pixmap] = (instance.position().x(), instance.position().y(),
                                         instance.size().width(), instance.size().height())
        return self.pixmap_boxes[pixmap]

    def fitWidget(self, pixmap, size):
        """The picture is scaled into the widget keeping its aspect ratio, so it is usually smaller than the
        widget - and the widget's rounded corners (cornerRadius) would sit on the empty part of the box instead
        of on the picture. Shrinking the widget to the picture, centered in the skin's box, puts them on it."""
        box_x, box_y, box_w, box_h = self.getBox(pixmap)
        width, height = box_w, box_h
        if size is not None and size.width() > 0 and size.height() > 0:
            width = min(size.width(), box_w)
            height = min(size.height(), box_h)
        pixmap.instance.move(ePoint(box_x + (box_w - width) // 2, box_y + (box_h - height) // 2))
        pixmap.instance.resize(eSize(width, height))

    def onPictureReady(self, path, pixmap, _picInfo=""):
        logger.info("...")
        ptr = self.picload_cache[path].getData()
        if ptr is not None:
            self.fitWidget(pixmap, ptr.size())
            pixmap.instance.setPixmap(ptr)
        else:
            self.fitWidget(pixmap, None)
            pixmap.instance.setPixmap(gPixmapPtr())
        self.picload_cache.pop(path, None)
        self.picload_conn_cache.pop(path, None)
