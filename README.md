# Wykorzystanie modeli TensorFlow na Raspberry Pi

### Opis
Analiza wykorzystywania wyuczonych modeli uczenia maszynowego na raspberry PI. Gromadzenie informacji na potrzebny pracy inn�ynierskiej.

### Konfiguracja �rodowiska
G��wnie b�dziemy pracowa� z `python`, dlatego rekomenduje instalacje �rodowiska wirtulanego, w kt�rym b�dziemy trzyma� wszystkie zainstalowane biblioteki przy pomocy `pip`. Dodatkowo poleca u�ycie `virtualnenvwrapper` aby trzyma� wszystkie �rodowiska wirtualne na komputerze w jednym miejsciu. Tutaj mog� wyst�pi� problemy z instalacj� na urz�dzeniu Raspberry spowodowane s�ab� kompatybilno�ci�. U mnie zadzia�o zainstlowanie `virtualenvwrapper` w wersji 4.8.4  z podanie numeru wersji podczas instalacji(`pip install virtualenvwrapper` nie dzia�a�o)): 
```
pip install virtualenvwrapper=="4.8.4"
```
Nast�pnie musimy edytowa� plik `.bashrc` dodaj�c nastepuj�ce wpisy:
```
export WORKON_HOME=$HOME/.virtualenvs
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh # path to virtualenvwrapper.sh (r�ne w zale�no�ci od systemu)
```
Od teraz przy pomocy `mkvirtualenv example_name` mo�emy utworzy� nowe wirtualne �rodowisko, aby je aktywowa� nale�y wykona� `workon example_name`.

### Tensorflow Lite
Dostarcza narz�dzia potrzbne to uruchomienia TensorFlow na urz�dzeniach mobilnych, IoT oraz urz�dzeniach osadzonych (z ang. embedded). 

1. Na pocz�tek potrzebujemy modelu TensorFlow. Jest struktura danych, kt�ra zawiera logik� i mechanizmy wyszkolnych sieci neuronwych. Taki model mo�emy sami wytrenowa� albo skorzysta� z wytrenowanych ju� modeli.**TensorFlow Lite nie udost�pnia narz�dzi do szkolenia modeli**. Przyk�adowe wy�wiczone modele dostarczone przez TensorFlow to: 

	* Klasyfikacja obraz�w
	* Wykrywanie obiekt�w
	* Inteligentne odpowiedzi
	* Pose estimation
	* Segmentation
	* Transfer stylu
	* Klasyfikacja tekstu
	* Pytania i odpowiedzi

	Sk�d jeszcze czerpa� modele: [TensorFlowHub](https://www.tensorflow.org/hub) . Przed skorzystanie nale�y przekonwertowa� te modele na format Lite.
	Modele r�wnie� mog� zosta� przetrenowane ponownie, jest to mniej z�o�ona operacja ni� wytrenowanie modelu od zera.

1. TensorFlow LIte jest stworzone aby wykorzysta� modele efektywnie na urz�dzenia ograniczonych w moc obliczeniow� i zasoby. Cz�� tej efektywno�ci mo�emy uzyskac poprzez stosowanie specjlanego formatu do przechowywaniu modelu.Konwersja jest obowi�zkowa dla TensorFlow Lite. Konwersja powoduje zmian� rozmiaru, wproawdza optymalizacje, ale nie wywiera wp�ywu na dok�adno��. Aby przekonwertowa� model musimy u�y� modu�u TensorFlow(nie Lite):
	```
		import tensorflow as tf

		converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
		tflite_model = converter.convert()
		open("converted_model.tflite", "wb").write(tflite_model)
	```
	
	Konwerter r�wnie� mo�emy uzyc z  poziomu linii polece�:
	```
		tflite_convert --saved_model_dir=/tmp/mobilenet_saved_model  --output_file=/tmp/mobilenet.tflite
	```

Aby wykorzysta� [TensorFlowLite](https://www.tensorflow.org/lite/guide)  na urz�dzeniu raspberry PI musimy zainstalowa� odpowiedni� wersj�. Pobrana wersja tak naprawd� udost�pnia jedynie interpreter do modeli. Poprawnie pe�nej wersji TensorFlow, a nie jedynie wersji Lite powodowa�o b��dy (pobiera�a si� wersja 1.x, gdzie aktualna wersja to 2.2):
```
pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
```
Opr�cz tej g��wnej biblioteki b�dziemy potrzebowa� `numpy` oraz `pillow`. Mo�emy je zainstalowa� przy pomocy zamieszczonego pliku `requirements.txt`:
```
pip install - r requirements.txt
```

Przyk�ad wykorzystania rozponowania obrazk�w:
```
https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/examples/python/
```
Aby dzia�a�o musimy poczyni� kilka zmian, poniewa� nie mamy zainstalowanego czystegoTensorflow. W folderze `image_recognition` jest przkeszta�cony plik z komentarzami opisuj�cymi dzia�anie programu. W tym ktalogu r�wnie� znajduj� si� przekszta�cony model zapisany w formacie `.tflite`, katalog `images` z przyk�adowymi obrazki do klasyfikacji oraz znaczniki. Aby uruchomi� program nale�y wykona�:
```
python image_recognition --model_file model.tflite --label_file labels.txt --image cat.png
```
Przyk�adowy output:
```
0.263747: 286:Egyptian cat
0.263291: 281:grey fox, gray fox, Urocyon cinereoargenteus
0.131645: 392:coho, cohoe, coho salmon, blue jack, silver salmon, Oncorhynchus kisutch
0.079361: 105:wallaby, brush kangaroo
0.044219: 278:red fox, Vulpes vulpes
```
Gdzie pierwsza kolumna to jest trafno�� modelu, a druga etykiety dopasowania.
