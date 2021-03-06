import pytest
import logging
from esprima import parseScript
from photoshop import PhotoshopConnection
from photoshop.protocol import Pixmap
from .mock import (
    script_output_server, subscribe_server, error_status_server, jpeg_server,
    pixmap_server, filestream_server, PASSWORD
)


class CallbackHandler(object):
    def __init__(self):
        self.count = 0

    def __call__(self, conn, data):
        assert data == b'{}'
        self.count += 1
        if self.count >= 3:
            return True
        return False


def test_subscribe(subscribe_server):
    with PhotoshopConnection(
        PASSWORD, port=subscribe_server[1], validator=parseScript
    ) as conn:
        conn.subscribe('imageChanged', CallbackHandler(), block=True)


def test_subscribe_error(error_status_server):
    with PhotoshopConnection(
        PASSWORD, port=error_status_server[1], validator=parseScript
    ) as conn:
        conn.subscribe('imageChanged', CallbackHandler(), block=True)


def test_get_document_thumbnail(jpeg_server):
    with PhotoshopConnection(
        PASSWORD, port=jpeg_server[1], validator=parseScript
    ) as conn:
        jpeg_binary = conn.get_document_thumbnail()
        assert isinstance(jpeg_binary, bytes)


def test_get_layer_thumbnail(pixmap_server):
    with PhotoshopConnection(
        PASSWORD, port=pixmap_server[1], validator=parseScript
    ) as conn:
        pixmap = conn.get_layer_thumbnail()
        assert isinstance(pixmap, Pixmap)


def test_get_layer_shape(script_output_server):
    with PhotoshopConnection(
        PASSWORD, port=script_output_server[1], validator=parseScript
    ) as conn:
        shape_info = conn.get_layer_shape()
        assert isinstance(shape_info, dict)


def test_get_document_info(script_output_server):
    with PhotoshopConnection(
        PASSWORD, port=script_output_server[1], validator=parseScript
    ) as conn:
        document_info = conn.get_document_info()
        assert isinstance(document_info, dict)


def test_get_document_stream(filestream_server):
    with PhotoshopConnection(
        PASSWORD, port=filestream_server[1], validator=parseScript
    ) as conn:
        document_info = conn.get_document_stream()
        assert isinstance(document_info, dict)
