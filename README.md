# Wykorzystanie modeli TensorFlow na Raspberry Pi

### Opis
Analiza wykorzystywania wyuczonych modeli uczenia maszynowego na raspberry PI. Gromadzenie informacji na potrzebny pracy inn¿ynierskiej.

### Konfiguracja ¶rodowiska
G³ównie bêdziemy pracowaæ z `python`, dlatego rekomenduje instalacje ¶rodowiska wirtulanego, w którym bêdziemy trzymaæ wszystkie zainstalowane biblioteki przy pomocy `pip`. Dodatkowo poleca u¿ycie `virtualnenvwrapper` aby trzymaæ wszystkie ¶rodowiska wirtualne na komputerze w jednym miejsciu. Tutaj mog± wyst±piæ problemy z instalacj± na urz±dzeniu Raspberry spowodowane s³ab± kompatybilno¶ci±. U mnie zadzia³o zainstlowanie `virtualenvwrapper` w wersji 4.8.4  z podanie numeru wersji podczas instalacji(`pip install virtualenvwrapper` nie dzia³a³o)): 
```
pip install virtualenvwrapper=="4.8.4"
```
Nastêpnie musimy edytowaæ plik `.bashrc` dodaj±c nastepuj±ce wpisy:
```
export WORKON_HOME=$HOME/.virtualenvs
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh # path to virtualenvwrapper.sh (ró¿ne w zale¿no¶ci od systemu)
```
Od teraz przy pomocy `mkvirtualenv example_name` mo¿emy utworzyæ nowe wirtualne ¶rodowisko, aby je aktywowaæ nale¿y wykonaæ `workon example_name`.

### Tensorflow Lite
Dostarcza narzêdzia potrzbne to uruchomienia TensorFlow na urz±dzeniach mobilnych, IoT oraz urz±dzeniach osadzonych (z ang. embedded). 

1. Na pocz±tek potrzebujemy modelu TensorFlow. Jest struktura danych, która zawiera logikê i mechanizmy wyszkolnych sieci neuronwych. Taki model mo¿emy sami wytrenowaæ albo skorzystaæ z wytrenowanych ju¿ modeli.**TensorFlow Lite nie udostêpnia narzêdzi do szkolenia modeli**. Przyk³adowe wyæwiczone modele dostarczone przez TensorFlow to: 

	* Klasyfikacja obrazów
	* Wykrywanie obiektów
	* Inteligentne odpowiedzi
	* Pose estimation
	* Segmentation
	* Transfer stylu
	* Klasyfikacja tekstu
	* Pytania i odpowiedzi

	Sk±d jeszcze czerpaæ modele: [TensorFlowHub](https://www.tensorflow.org/hub) . Przed skorzystanie nale¿y przekonwertowaæ te modele na format Lite.
	Modele równie¿ mog± zostaæ przetrenowane ponownie, jest to mniej z³o¿ona operacja ni¿ wytrenowanie modelu od zera.

1. TensorFlow LIte jest stworzone aby wykorzystaæ modele efektywnie na urz±dzenia ograniczonych w moc obliczeniow± i zasoby. Czê¶æ tej efektywno¶ci mo¿emy uzyskac poprzez stosowanie specjlanego formatu do przechowywaniu modelu.Konwersja jest obowi±zkowa dla TensorFlow Lite. Konwersja powoduje zmianê rozmiaru, wproawdza optymalizacje, ale nie wywiera wp³ywu na dok³adno¶æ. Aby przekonwertowaæ model musimy u¿yæ modu³u TensorFlow(nie Lite):
	```
		import tensorflow as tf

		converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
		tflite_model = converter.convert()
		open("converted_model.tflite", "wb").write(tflite_model)
	```
	
	Konwerter równie¿ mo¿emy uzyc z  poziomu linii poleceñ:
	```
		tflite_convert --saved_model_dir=/tmp/mobilenet_saved_model  --output_file=/tmp/mobilenet.tflite
	```

Aby wykorzystaæ [TensorFlowLite](https://www.tensorflow.org/lite/guide)  na urz±dzeniu raspberry PI musimy zainstalowaæ odpowiedni± wersjê. Pobrana wersja tak naprawdê udostêpnia jedynie interpreter do modeli. Poprawnie pe³nej wersji TensorFlow, a nie jedynie wersji Lite powodowa³o b³êdy (pobiera³a siê wersja 1.x, gdzie aktualna wersja to 2.2):
```
pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
```
Oprócz tej g³ównej biblioteki bêdziemy potrzebowaæ `numpy` oraz `pillow`. Mo¿emy je zainstalowaæ przy pomocy zamieszczonego pliku `requirements.txt`:
```
pip install - r requirements.txt
```

Przyk³ad wykorzystania rozponowania obrazków:
```
https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/examples/python/
```
Aby dzia³a³o musimy poczyniæ kilka zmian, poniewa¿ nie mamy zainstalowanego czystegoTensorflow. W folderze `image_recognition` jest przkeszta³cony plik z komentarzami opisuj±cymi dzia³anie programu. W tym ktalogu równie¿ znajduj± siê przekszta³cony model zapisany w formacie `.tflite`, katalog `images` z przyk³adowymi obrazki do klasyfikacji oraz znaczniki. Aby uruchomiæ program nale¿y wykonaæ:
```
python image_recognition --model_file model.tflite --label_file labels.txt --image cat.png
```
Przyk³adowy output:
```
0.263747: 286:Egyptian cat
0.263291: 281:grey fox, gray fox, Urocyon cinereoargenteus
0.131645: 392:coho, cohoe, coho salmon, blue jack, silver salmon, Oncorhynchus kisutch
0.079361: 105:wallaby, brush kangaroo
0.044219: 278:red fox, Vulpes vulpes
```
Gdzie pierwsza kolumna to jest trafno¶æ modelu, a druga etykiety dopasowania.
