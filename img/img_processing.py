from PIL import Image

def rotate_image_180(input_path, output_path):
    """
    将图片旋转180度并保存

    参数:
        input_path (str): 输入图片路径
        output_path (str): 输出图片路径
    """
    try:
        # 打开图片文件
        with Image.open(input_path) as img:
            # 旋转180度
            rotated_img = img.rotate(180)

            # 保存旋转后的图片
            rotated_img.save(output_path)
            print(f"图片已成功旋转180度并保存到 {output_path}")

    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_path}")
    except Exception as e:
        print(f"处理图片时发生错误: {e}")

# 使用示例
input_image = "white_down_arrow.png"  # 替换为你的输入图片路径
output_image = "white_up_arrow.png"  # 输出图片路径

rotate_image_180(input_image, output_image)
