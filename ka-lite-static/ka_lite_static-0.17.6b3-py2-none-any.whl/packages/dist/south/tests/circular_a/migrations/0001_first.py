from south.db import db
from django.db import models

class Migration:
    
    depends_on = [('circular_b', '0001_first')]
    
    def forwards(self):
        pass
    
    def backwards(self):
        pass

