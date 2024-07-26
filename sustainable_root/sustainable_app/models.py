from django.db import models
from django.utils import timezone
from datetime import timedelta

class Task(models.Model):
    name = models.CharField(max_length=200)
    recurring_rate = models.PositiveIntegerField(default=1)
    last_done = models.DateField(null=True, blank=True)
    next_due = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)  # Add completed field

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set next_due when creating a new task
            self.next_due = timezone.now().date() + timedelta(days=self.recurring_rate)
        else:
            if self.completed:  # Reset next_due based on last_done when task is marked as completed
                self.last_done = timezone.now().date()
                self.next_due = self.last_done + timedelta(days=self.recurring_rate)
                self.completed = False  # Reset completed status after setting next_due
        super().save(*args, **kwargs)

    def is_overdue(self):
        return timezone.now().date() > self.next_due

    def overdue_days(self):
        if self.is_overdue():
            return (timezone.now().date() - self.next_due).days
        return 0

    def should_display_overdue(self):
        return self.overdue_days() <= (self.recurring_rate / 3)

    def get_display_info(self):
        overdue_indicator = '!' if self.is_overdue() else ''
        return {
            'name': self.name,
            'next_due': self.next_due,
            'is_overdue': self.is_overdue(),
            'overdue_days': self.overdue_days(),
            'should_display_overdue': self.should_display_overdue(),
            'overdue_indicator': overdue_indicator,
            'completed': self.completed  # Include completed status in display info
        }
    
    def mark_as_completed(self):
        self.completed = True
        self.save()
