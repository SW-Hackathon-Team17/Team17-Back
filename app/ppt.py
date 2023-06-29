from pptx import Presentation

def save_pptx_as_images(pptx_file):
    # PPT 파일을 열기
    presentation = Presentation(pptx_file)

    # 각 슬라이드에 대해 반복하며 이미지 저장
    for slide_num, slide in enumerate(presentation.slides):
        # 슬라이드 이미지 저장
        slide.export(f'slide{slide_num + 1}.png')

        # 또는 원하는 다른 이미지 포맷으로 저장할 수도 있습니다.
        # slide.export(f'slide{slide_num + 1}.jpg', 'JPEG')

        print(f'Saved slide {slide_num + 1} as image.')

# PPT 파일 경로
pptx_file = 'example.pptx'

# 함수 호출
save_pptx_as_images(pptx_file)