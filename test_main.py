import io
from fastapi.testclient import TestClient
from main import app
from files import s3, AWS_S3_BUCKET_NAME

client = TestClient(app)


def test_get_file():
    file_content = b'example file content'
    file = io.BytesIO(file_content)
    key = 'test_key'
    s3().upload_fileobj(file, AWS_S3_BUCKET_NAME, key)

    response = client.get(f'/{key}')
    assert response.status_code == 200
