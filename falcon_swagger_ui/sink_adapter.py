import os
import falcon
import mimetypes
import aiofiles


class StaticSyncSinkAdapter(object):

    def __init__(self, static_path):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.static_dir = os.path.join(curr_dir, static_path)
    
    def _check_for_folder(self, resp, filepath):
        resp.content_type = mimetypes.guess_type(filepath)[0]
        file_path = os.path.normpath(
            os.path.join(self.static_dir, filepath)
        )
        if not file_path.startswith(self.static_dir + os.sep):
            raise falcon.HTTPNotFound()
        if not os.path.exists(file_path):
            raise falcon.HTTPNotFound()
        return file_path

    def __call__(self, req, resp, filepath):
        
        file_path = self._check_for_folder(resp, filepath)

        stream = open(file_path, 'rb')
        stream_len = os.path.getsize(file_path)
        resp.set_stream(stream, stream_len)


class StaticAsyncSinkAdapter(StaticSyncSinkAdapter):

    async def __call__(self, req, resp, filepath):

        file_path = self._check_for_folder(resp, filepath)
        resp.stream = await aiofiles.open(file_path, 'rb')