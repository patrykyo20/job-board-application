import django.db.models.deletion
from django.db import migrations, models
import django.utils.timezone  # Import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='changedAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),  # Correct default
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='jobApplication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='api.job'),
        ),
        migrations.AddField(
            model_name='user',
            name='jobOfferPosted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_offers', to='api.job'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.location'),
        ),
    ]
