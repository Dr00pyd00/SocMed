
# Images avec Django

On stock pas les images dans la table on stock le path vers le disk qui contient les data.

## Dams Settings.py:

```python 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
- MEDIA_ROOT = la on est le dossier ou sont stocker les images
- MEDIA_URL = prefic URL pour acceder a une image 

### ATTENTION en prod on fait pas ca pour gerer les images 

En dev : 

```python 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... tes routes existantes ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Exemple de champ

```python 
avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
```

- `upload_to` = dans quel sous dossier ranger l'image


## Installations / Prerequis:

```bash 
pip install Pillow
pip freeze > requirements.txt
```




