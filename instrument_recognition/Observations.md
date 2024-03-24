# Model Results

## Original Model

|Model Type|Optimizer|Loss|Metrics|
|----------|---------|----|-------|
Sequential CNN|adam|categorical_crossentropy|accuracy


|Layer | Parameter 1 | Parameter 2 | Activation|
|-----:|-------------|-------------|-----------|
|Conv2D|filters=32|kernel_size=(3,3)|relu|
|MaxPooling||pool_size=(2,2)||
|Conv2D|filters=64|kernel_size=(3,3)|relu|
|MaxPooling||pool_size=(2,2)||
|Conv2D|filters=128|kernel_size=(3,3)|relu|
|MaxPooling||pool_size=(2,2)||
|Flatten||||
|Dropout|rate=0.5|||
|Dense|units=64||relu|
|Dense|units=11||softmax|

|Result | Normalized Data | Augmented Data |
|------:|-----------------|----------------|
|Loss: |0.4359|0.2570|
|Accuracy:|0.8482|0.9145|
|Val. Loss:|1.7061|0.9200|
|Val. Accuracy:|0.5690|0.7934|

Augmented data methods: Use stereo audio, add noise, pitch shift, swap channels (stereo audio)

## Altered Model

// TODO


