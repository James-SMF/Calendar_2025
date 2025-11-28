from PIL import Image, ImageOps

def invert_image(input_path, output_path):
    """
    反色图片（黑色变白色，白色变黑色）

    参数:
        input_path (str): 输入图片路径
        output_path (str): 输出图片路径
    """
    try:
        with Image.open(input_path) as img:
            # 如果是RGBA（带透明通道），先转换为RGB再反色
            if img.mode == 'RGBA':
                rgb_img = img.convert('RGB')
                inverted_img = ImageOps.invert(rgb_img)
                inverted_img = inverted_img.convert('RGBA')  # 转回RGBA
                # 保持原始透明度
                inverted_img.putalpha(img.getchannel('A'))
            else:
                inverted_img = ImageOps.invert(img)

            inverted_img.save(output_path)
            print(f"图片已成功反色并保存到 {output_path}")

    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_path}")
    except Exception as e:
        print(f"处理图片时发生错误: {e}")

# 使用示例
input_image = "white_down_arrow.png"  # 替换为你的输入图片路径
output_image = "black_down_arrow.png"  # 输出图片路径

invert_image(input_image, output_image)
