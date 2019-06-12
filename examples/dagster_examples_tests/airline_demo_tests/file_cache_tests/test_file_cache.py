import io

from botocore.exceptions import ClientError

from dagster.seven import mock
from dagster_examples.airline_demo.file_cache import S3FileCache, S3FileHandle


def test_s3_file_cache_file_not_present():
    session_mock = mock.MagicMock()
    session_mock.get_object.side_effect = ClientError({}, None)
    file_store = S3FileCache(
        s3_bucket='some-bucket', s3_key='some-key', s3_session=session_mock, overwrite=False
    )

    assert not file_store.has_file_object('foo')

    session_mock.get_object.assert_called_once_with(
        Bucket='some-bucket', Key=file_store.get_full_key('foo')
    )


def test_s3_file_cache_file_present():
    session_mock = mock.MagicMock()
    file_store = S3FileCache(
        s3_bucket='some-bucket', s3_key='some-key', s3_session=session_mock, overwrite=False
    )

    assert file_store.has_file_object('foo')

    session_mock.get_object.assert_called_once_with(
        Bucket='some-bucket', Key=file_store.get_full_key('foo')
    )


def test_s3_file_cache_correct_handle():
    file_store = S3FileCache(
        s3_bucket='some-bucket', s3_key='some-key', s3_session=mock.MagicMock(), overwrite=False
    )

    assert isinstance(file_store.get_file_handle('foo'), S3FileHandle)


def test_s3_file_cache_write_file_object():
    session_mock = mock.MagicMock()
    file_store = S3FileCache(
        s3_bucket='some-bucket', s3_key='some-key', s3_session=session_mock, overwrite=False
    )

    stream = io.BytesIO('content'.encode())
    file_store.write_file_object('foo', stream)

    session_mock.put_object.assert_called_once_with(
        Bucket='some-bucket', Key=file_store.get_full_key('foo'), Body=stream
    )
