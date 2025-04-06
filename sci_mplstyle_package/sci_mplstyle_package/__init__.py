# __init__.py
import matplotlib.pyplot as plt
import os

style_path = os.path.join(os.path.dirname(__file__), 'style_files', 'publication.mplstyle')
plt.style.use(style_path)
