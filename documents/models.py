from django.db import models
from microsys.models import ScopedModel

class Document(ScopedModel):
    is_section=True
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # form_exclude = ["id", "uploaded_at"]
    # table_exclude = ["id", "uploaded_at"]

    def __str__(self):
        return self.title

class SubAffiliate(ScopedModel):
    """Model representing a sub-affiliate (AffiliateDepartment)."""
    name = models.CharField(max_length=255, verbose_name="اسم القسم التابع لجهة")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "قسم تابع لجهة"
        verbose_name_plural = "الأقسام التابعة لجهة"
        ordering = ['id']
        default_permissions = ()
    
    def __str__(self):
        return self.name


class AffiliateDepartment(ScopedModel):
    """Junction model relating Affiliate and SubAffiliate (Department)."""
    affiliate = models.ForeignKey('Affiliate', on_delete=models.CASCADE)
    sub_affiliate = models.ForeignKey(SubAffiliate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('affiliate', 'sub_affiliate')
        verbose_name = "قسم تابع لجهة"
        verbose_name_plural = "الأقسام التابعة لجهات"
        default_permissions = ()

    def __str__(self):
        return f"{self.affiliate.name} - {self.sub_affiliate.name}"


class Affiliate(ScopedModel):
    """Model representing an affiliate entity."""
    is_section=True
    type = models.CharField(max_length=50, choices=[
        ('Council', 'مجلس'),
        ('Ministry', 'وزارة'),
        ('Authority', 'هيئة'),
        ('Agency', 'مصلحة'),
        ('Company', 'شركة'),
        ('Affiliated', 'جهة تابعة'),
        ('Other', 'جهات أخرى')
    ], verbose_name="نوع الجهة")
    name = models.CharField(max_length=255, unique=True, verbose_name="الاسم")
    
    sub_affiliates = models.ManyToManyField(SubAffiliate, blank=True, through='AffiliateDepartment', related_name='affiliates', verbose_name="الأقسام التابعة")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # form_exclude = ["id", "created_at", "updated_at"]
    # table_exclude = ["id", "created_at", "updated_at"]

    class Meta:
        verbose_name = "جهة"
        verbose_name_plural = "الجهات الاخرى"
        ordering = ['id']
        default_permissions = ()
    
    def __str__(self):
        return self.name

