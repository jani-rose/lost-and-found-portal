from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    REPORT_TYPES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Recovered', 'Recovered'),
        ('Given Away', 'Given Away'),
        ('Closed', 'Closed'),
    ]

    CATEGORY_CHOICES = [
        # Electronics
        ('Mobile Phones', 'Mobile Phones'),
        ('Laptops', 'Laptops'),
        ('Earphones', 'Earphones'),
        ('Chargers', 'Chargers'),
        ('Power Banks', 'Power Banks'),

        # Documents
        ('Student ID Cards', 'Student ID Cards'),
        ('Aadhaar Cards', 'Aadhaar Cards'),
        ('Driving Licenses', 'Driving Licenses'),
        ('Other Documents', 'Other Documents'),

        # Personal Belongings
        ('Wallets', 'Wallets'),
        ('Keys', 'Keys'),
        ('Watches', 'Watches'),
        ('Umbrellas', 'Umbrellas'),

        # Academic Items
        ('Books', 'Books'),
        ('Stationery', 'Stationery'),

        # Others
        ('Bags', 'Bags'),
        ('Water Bottles', 'Water Bottles'),
        ('Miscellaneous Items', 'Miscellaneous Items'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()

    LOCATION_CHOICES = [
        ('Library', 'Library'),
        ('Food Court', 'Food Court'),
        ('Hostel', 'Hostel'),
        ('Academic Block A', 'Academic Block A'),
        ('Academic Block B', 'Academic Block B'),
        ('Parking Area', 'Parking Area'),
        ('Bus Stop', 'Bus Stop'),
        ('Other', 'Other'),
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=100,
        choices=LOCATION_CHOICES
        )

    report_type = models.CharField(
        max_length=10,
        choices=REPORT_TYPES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    image = models.ImageField(
        upload_to='items/',
        blank=True,
        null=True
    )

    event_date = models.DateField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} on {self.item.title if self.item else 'general'}"