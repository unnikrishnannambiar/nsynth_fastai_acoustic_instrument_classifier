# AUTOGENERATED! DO NOT EDIT! File to edit: app.ipynb.

# %% auto 0
__all__ = ['learn', 'categories', 'aud', 'examples', 'intf', 'log_mel_spec_tfm', 'classify_aud']

# %% app.ipynb 1
def log_mel_spec_tfm(fname, src_path, dst_path):
    os.makedirs(str(dst_path), exist_ok = True)
    y, sr = librosa.load(str(src_path/fname), mono=True)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
                                  sr=sr)
    plt.savefig(str(dst_path/fname[:-4]) + '.png')
    plt.close()
    return img

# %% app.ipynb 2
learn = load_learner('model.pkl')
learn.remove_cb(ProgressCallback)

# %% app.ipynb 6
categories = ('Brass', 'Flute', 'Guitar', 'Keyboard', 'Mallet', 'Reed', 'String', 'Vocal')

def classify_aud(aud):
    log_mel_spec_tfm(aud, Path('.'), Path('.'))
    img_fname = str(aud[:-4]) + '.png'
    pred, idx, probs = learn.predict(img_fname)
    return dict(zip(categories, map(float, probs)))

# %% app.ipynb 8
aud = gr.Audio(source="upload", type="numpy")
examples = ['test/' + str(f.name) for f in Path('test').iterdir()]

intf = gr.Interface(fn = classify_aud, inputs = aud, outputs = "label", examples = examples)
intf.launch(inline = False)
