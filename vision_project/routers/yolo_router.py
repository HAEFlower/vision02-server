import io
import logging
import os
from datetime import datetime
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from PIL import Image, ImageDraw, ImageFont
from ..models.yolo_model import load_model, run_inference
from ..domain.openai.request_gpt import ask_chatgpt

router = APIRouter()
yolo_model = load_model()


def save_annotated_image(image, result, INGREDIENTS, save_dir="results"):
    """바운딩 박스가 그려진 이미지 저장 함수"""
    try:
        draw = ImageDraw.Draw(image)

        # 시스템 기본 폰트 사용으로 수정
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
            logging.warning("Arial font not found, using default font")

        os.makedirs(save_dir, exist_ok=True)

        for box in result[0].boxes:
            cords = box.xyxy[0].tolist()
            xmin, ymin, xmax, ymax = map(int, cords)

            draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=(255, 0, 0), width=2)

            cls_id = int(box.cls.item())
            label = get_ingredient_by_id(INGREDIENTS, cls_id)
            conf = box.conf.item()
            text = f"{label} {conf:.2f}"
            draw.text((xmin, ymin - 25), text, fill=(255, 0, 0), font=font)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(save_dir, f"detection_{timestamp}.jpg")
        image.save(output_path)
        logging.info(f"Annotated image saved to: {output_path}")

    except Exception as e:
        logging.error(f"Image annotation failed: {str(e)}")
        raise


@router.post("/")
async def vision_inference(
    file: UploadFile = File(...),
    cookingGoal: str = Form(...),
    cookingMethod: str = Form(...),
):
    """머신 비전 추론 엔드포인트"""
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        logging.info(f"Image processing completed: {file.filename}")

        result = run_inference(yolo_model, image)
        logging.info(f"Inference completed: {file.filename}")
        INGREDIENTS = [result[0].names[i] for i in range(50)]

        # 바운딩 박스가 포함된 이미지 저장
        save_annotated_image(image, result, INGREDIENTS)

        class_ids = []
        if hasattr(result[0], "boxes"):
            for box in result[0].boxes:
                cls_id = int(box.cls.item())
                class_ids.append(cls_id)

        ingredients = get_ingreidients_list_by_ids(INGREDIENTS, class_ids)
        logging.info(f"Inference results: {ingredients}")

        response = ask_chatgpt(ingredients, cookingGoal, cookingMethod)
        logging.info(f"ChatGPT response generated")

        return response

    except Exception as e:
        logging.error(f"Processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def get_ingredient_by_id(INGREDIENTS, ingredient_id: int) -> str:
    return INGREDIENTS[ingredient_id]


def get_ingreidients_list_by_ids(INGREDIENTS, ids: list) -> list:
    return [get_ingredient_by_id(INGREDIENTS, ingredient_id) for ingredient_id in ids]
