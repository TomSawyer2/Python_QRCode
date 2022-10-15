Image = None
ImageDraw = None

try:
    from PIL import Image, ImageDraw
except ImportError:
    try:
        import Image
        import ImageDraw
    except ImportError:
        pass
