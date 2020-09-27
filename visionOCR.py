from google.cloud import vision
import io
import os
key = 'AIzaSyDbE9YL4nXp9O1U3AeD0LY5CEzAnUOoYd4'
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.curdir, dir_path+'/rpaocr-283109-9fa5ddb77e44.json')
def detect_text(pagename):
    """Detects text in the file."""

    path = pagename
    imageContext = key
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(
        image=image,
        image_context={"language_hints": ["bn"]},  # Bengali
    )
    # response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    nid_info= []
    f = open("test3_output.txt", "a", encoding="utf-8")
    for text in texts:
        print('\n"{}"'.format(text.description))

        f.write(text.description)

        nid_info.append('\n"{}"'.format(text.description).replace('\n', '#'))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        f.write('bounds: {}'.format(','.join(vertices)))
    f.close()
    return nid_info
dir_path = os.path.dirname(os.path.realpath(__file__))
filename= dir_path +'\\test3.png'
nid_info= detect_text(filename)
print(nid_info)
print(len(nid_info))