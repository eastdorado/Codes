from PIL import Image,ImageFilter,ImageGrab,ImageDraw,ImageFont

# 创建图片：宽800*高600，红色
imNew = Image.new('RGB',(800,600),(255,0,0))

# 显示图片
#imNew.show()

# 抓取屏幕
imGrab = ImageGrab.grab()
imGrab.save('grab.jpg', 'jpeg')

# 打开图片
im = Image.open(r'timg4.jpeg')
im1 = Image.open(r'1_transpose.jpeg')

# 复制图片
im1 = im.copy()
im2 = im.copy()
im3 = im.copy()
im4 = im.copy()
im5 = im.copy()
im6 = im.copy()
im7 = im.copy()

# 获得图片宽高:
w, h = im.size
print('图片宽高:{} * {}'.format(w, h))

# 缩略图（图片不会被拉伸，只能缩小）
# im.thumbnail((w//2, h//2))
# im.save('1_thumbnail.jpg', 'jpeg')

# 缩放（图片可能会被拉伸，可缩小也可放大）
# im1 = im1.resize((w//2, h//2))
# im1.save('1_resize.jpg', 'jpeg')

# 模糊图片
# im2 = im2.filter(ImageFilter.BLUR)
# im2.save('1_blur.jpg', 'jpeg')

# 旋转图片，逆时钟旋转45度
# im3 = im3.rotate(45)
# im3.save('1_rotate.jpg', 'jpeg')

# 图片转换：左右转换 FLIP_LEFT_RIGHT，上下转换 FLIP_TOP_BOTTOM
im4 = im4.transpose(Image.FLIP_LEFT_RIGHT)
im4.save('1_transpose.jpeg', 'jpeg')

# 图片裁剪
# box = (200,200,400,400) #左上角(0,0)，4元组表示坐标位置：左、上、右、下
# im5 = im5.crop(box)
# im5.save('1_crop.jpg', 'jpeg')

# 图片上添加文字
# draw = ImageDraw.Draw(im6)
# #truetype设置字体、文字大小
# #stxingka.ttf华文行楷 simkai.ttf 楷体 simli.ttf 隶书
# font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\stxingka.ttf", 20)
# draw.text((100,100), ('hello word \n你好，世界'), fill='#0000ff', font=font)
# im6.save('1_drawText.jpg', 'jpeg')

# 图片上添加图片（粘贴图片）
# imTmp = Image.new('RGB',(30,30),'blue')
# im7.paste(imTmp, (50,50)) #第2个参数为坐标
# im7.save('1_paste.jpg','jpeg')


# 图片横向拼接：拼接上面im6、im7（两张图片大小一样）
im6Width, im6Height = im1.size
imHorizontal = Image.new('RGB', (im6Width * 2, im6Height))
imHorizontal.paste(im1, (0, 0))
imHorizontal.paste(im4, (im6Width, 0))
imHorizontal.save('1_horizontal.jpg', 'jpeg')

# 图片竖向拼接：拼接上面im6、im7
# imVertical = Image.new('RGB', (im6Width, im6Height*2))
# imVertical.paste(im6, (0,0))
# imVertical.paste(im7, (0,im6Height))
# imVertical.save('1_vertical.jpg', 'jpeg')