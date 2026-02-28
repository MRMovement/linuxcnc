"""文本工具"""

def has_chinese(text):
    """判断是否包含汉字"""
    if not text:
        return False
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

def create_html_button_text(text, icon_filename=None):
    """创建按钮的HTML内容"""
    from src.utils.image_loader import image_to_base64
    
    if not text and not icon_filename:
        return ""
    
    # 构建文字部分
    text_html = ""
    if text:
        if text.isalpha() and len(text) == 1:
            if icon_filename:
                text_html = f"<div style='font-size: 20pt; font-weight: bold;'>{text}</div>"
            else:
                text_html = f"<div style='font-size: 25pt; font-weight: bold;'>{text}</div>"
        elif has_chinese(text):
            # 处理中文文本
            chinese_chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
            if chinese_chars:
                if len(chinese_chars) == 4:
                    line1 = f"{chinese_chars[0]}{chinese_chars[1]}"
                    line2 = f"{chinese_chars[2]}{chinese_chars[3]}"
                    text_html = f"""
                        <div style='font-size: 16pt; font-weight: bold; line-height: 1;'>
                            <div>{line1}</div>
                            <div>{line2}</div>
                        </div>
                    """
                else:
                    lines = []
                    for i in range(0, len(chinese_chars), 2):
                        line = ''.join(chinese_chars[i:i+2])
                        lines.append(f"<span style='font-size: 17pt; font-weight: bold;'>{line}</span>")
                    chinese_html = "<br>".join(lines)
                    text_html = f"<div style='line-height: 1.0;'>{chinese_html}</div>"
        else:
            text_html = f"<div style='font-size: 17pt; font-weight: bold;'>{text}</div>"
    
    # 构建图片部分
    img_html = ""
    if icon_filename and icon_filename.lower().endswith('.png'):
        encoded_image = image_to_base64(icon_filename)
        if encoded_image:
            img_html = f"""
                <div style='
                    margin-top: 5px; 
                    height: 45px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    overflow: hidden;
                '>
                    <img src='data:image/png;base64,{encoded_image}' 
                        style='
                            max-height: 100%;
                            max-width: 100%;
                            object-fit: contain;
                        '>
                </div>
            """
    
    # 构建完整HTML
    if img_html:
        return f"""
            <div style='
                text-align: center; 
                padding: 5px;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            '>
                <div>{text_html}</div>
                <div>{img_html}</div>
            </div>
        """
    else:
        return f"""
            <div style='
                text-align: center; 
                padding: 5px;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            '>
                <div>{text_html}</div>
            </div>
        """