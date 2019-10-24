from django.db import models
#导入内建的user模型
from django.contrib.auth.models import User
#timezone 
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image

class ArticleColumn(models.Model):
    # 栏目
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
        
# Blog article data models
class ArticlePost(models.Model):
    """文章作者
    argument: on_delete 删除指定数据的方式
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    """文章标题
    models.CharFied 字符串字段，用于保存较短的字符串
    """
    title = models.CharField(max_length=100)

    """
    文章正文 保存大量文本
    """
    body = models.TextField()

    """文章创建时间
    default=timezone.now 指定创建文章是的时间
    """
    created = models.DateTimeField(default=timezone.now)

    """文章更新时间
    auto_now = true 指定每次数据更新时的时间
    """
    update = models.DateTimeField(auto_now=True)

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 处理标题图
     # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        # //@ts-ignore
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    # 文章浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 文章栏目一对多外键
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article')
    """
    内部类 class meta 用于给 model 定义元数据
    """
    class Meta:
        #ordering 指定模型返回的数据
        # -created 表明数据应该用倒序排列
        ordering = ('-created',)
    """
    函数 __str__ 定义当调用对象的str() 方法时 返回值
    """
    def __str__(self):
        # 返回标题
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    