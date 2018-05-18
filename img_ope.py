from PIL import Image
import pytesseract

class img_operate(object):
    def split_img(self,url):
        im = Image.open(url)
        tips_image = im.crop((0, 344, 116, 383))
        tips_image.save('tips.png')
        bg_image = im.crop((0, 0, 344, 344))
        bg_image.save("bg_img.png")

    def recog_tips(self,url):
        tips = []
        str = pytesseract.image_to_string(Image.open(url), lang='chi_sim')
        for i in str:
            if(i!=' '):
                tips.append(i)
        return tips

    def recog_bg(self,tips_url,bg_url):
        tips = self.recog_tips(tips_url)
        str = pytesseract.image_to_string(Image.open(bg_url),lang='chi_sim')
        print(str)

    #def gray_bg(self,bg_url):




if __name__ == '__main__':
    test = img_operate().split_img(url='F:\images\gee_img_0.jpg')
    #print(img_operate().recog_bg('tips.png','bg_img.png'))
    str = pytesseract.image_to_string(Image.open('test.png'),lang='chi_sim')
    print(str)