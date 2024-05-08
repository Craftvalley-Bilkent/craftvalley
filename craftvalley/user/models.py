from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    active = models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')])

class SmallBusiness(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    business_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    picture = models.BinaryField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.BinaryField(null=True, blank=True)
    payment_info = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    images = models.BinaryField(null=True, blank=True)

class BalanceRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    record_date = models.DateField()
    record_type = models.CharField(max_length=255)
    record_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Recipient(models.Model):
    recipient_id = models.AutoField(primary_key=True)
    recipient_name = models.CharField(max_length=255, unique=True)

class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    material_name = models.CharField(max_length=255, unique=True)

class MainCategory(models.Model):
    main_category_id = models.AutoField(primary_key=True)
    main_category_name = models.CharField(max_length=255)

class SubCategory(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)

class InCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

class HasReported(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    small_business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE)
    report_description = models.CharField(max_length=255)
    report_date = models.DateField()

class Ban(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    small_business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE)
    ban_duration = models.CharField(max_length=255)
    ban_date = models.DateField()

class SystemReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_title = models.CharField(max_length=255)
    report_date = models.DateField()
    report_results = models.CharField(max_length=255)

class CreateReport(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    system_report = models.ForeignKey(SystemReport, on_delete=models.CASCADE)

class Rate(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star = models.DecimalField(max_digits=2, decimal_places=1)

class Wish(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class AddToShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

class SelectProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class BusinessHasRecord(models.Model):
    small_business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE)
    balance_record = models.ForeignKey(BalanceRecord, on_delete=models.CASCADE)

class CustomerHasRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance_record = models.ForeignKey(BalanceRecord, on_delete=models.CASCADE)

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    small_business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    count = models.IntegerField()
    transaction_status = models.CharField(max_length=255)

class AddAmount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    small_business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE)
    amount = models.IntegerField()

class AddProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    small_business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE)
    post_date = models.DateField()

class MadeBy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

class IsFor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
