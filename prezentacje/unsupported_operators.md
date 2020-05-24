### 2
TensorFlow Lite obsługuje wiele operacji TensorFlow używanych we wspólnych modelach wnioskowania. Ponieważ są one przetwarzane przez konwerter optymalizujący TensorFlow Lite, operacje te mogą być pomijane lub łączone, zanim obsługiwane operacje zostaną odwzorowane na ich odpowiedniki TensorFlow Lite.

Ponieważ zestaw operacji TensorFlow Lite jest mniejszy niż TensorFlow, nie każdy model można przekształcić. Nawet w przypadku obsługiwanych operacji czasami ze względu na wydajność oczekuje się bardzo specyficznych wzorców użytkowania. Oczekujemy, że rozszerzymy zestaw obsługiwanych operacji w przyszłych wersjach TensorFlow Lite. Dodatkowe operacje mogą być uwzględnione przy użyciu wybranych operacji TensorFlow, kosztem rozmiaru binarnego.

Najlepszym sposobem na zrozumienie, jak zbudować model TensorFlow, który może być używany z TensorFlow Lite, jest dokładne rozważenie sposobu konwersji i optymalizacji operacji oraz ograniczeń nałożonych przez ten proces

### 3

Większość operacji TensorFlow Lite jest ukierunkowana zarówno na wnioskowanie zmiennoprzecinkowe (float32), jak i kwantyzowane (uint8, int8), ale wiele operacji jeszcze nie działa dla innych typów, takich jak tf.float16 i łańcuchy.

Oprócz używania różnych wersji operacji, inna różnica między modelami zmiennoprzecinkowymi a modelami kwantyzowanymi polega na sposobie ich konwersji. Skwantyzowana konwersja wymaga informacji o zakresie dynamicznym dla tensorów. Wymaga to „fałszywej kwantyzacji” podczas treningu modelowego, uzyskiwania informacji o zakresie za pomocą zestawu danych kalibracyjnych lub dokonywania oszacowania „w locie”. Zobacz kwantyzację.

### 4
Kwantyzacja polega na zmniejszeniu precyzji liczb używanych do przedstawienia parametrów modelu, które domyślnie są 32-bitowymi liczbami zmiennoprzecinkowymi. Powoduje to mniejszy rozmiar modelu i szybsze obliczenia.

### 5
Jednostka przetwarzająca tensor (TPU) to specyficzny dla aplikacji układ scalony akceleratora AI (ASIC) opracowany przez Google specjalnie do uczenia maszynowego w sieciach neuronowych, szczególnie przy użyciu własnego oprogramowania TensorFlow firmy Google. Google zaczął korzystać z TPU wewnętrznie w 2015 r., Aw 2018 r. Udostępnił je do użytku stronom trzecim, zarówno jako część swojej infrastruktury chmurowej, jak i oferując mniejszą wersję układu na sprzedaż(**EDGE TPU**).


### 6
Format danych i emisja

W tej chwili TensorFlow Lite obsługuje tylko format „NHWC” TensorFlow, a transmisja jest obsługiwana tylko w ograniczonej liczbie operacji (tf.add, tf.mul, tf.sub i tf.div).

**Transmisja** - połączenie dwóch tablic o różnych rozmiarach przy pomocy operacji arytmetycznych w jedną tablicę.

### 7
Następujące operacje TensorFlow są zwykle mapowane na ich odpowiedniki TensorFlow Lite:

    tf.batch_to_space_nd - O ile tensor wejściowy ma wartość 4D (1 partia + 2 przestrzenne + 1 inna), a atrybut uprawy nie jest używany.
    tf.exp
    tf.fake_quant
    tf.matmul - ponieważ drugi argument jest stały i transpozycja nie jest używana *
    tf.nn.avg_pool
    tf.nn.conv2d - O ile filtr jest stały.
    tf.nn.depthwise_conv2d - Tak długo, jak filtr jest stały, a współczynnik wynosi [1, 1].
    tf.nn.l2_normalize - Dopóki normalizacja odbywa się wzdłuż ostatniego wymiaru.
    tf.nn.local_response_normalization
    tf.nn.log_softmax - O ile oś nie jest podana.
    tf.nn.max_pool
    tf.nn.softmax - o ile tensory są 2D, a oś jest ostatnim wymiarem.
    tf.nn.top_k
    tf.one_hot
    tf.pad - pod warunkiem, że nie są używane tryb i wartości stałe.
    tf.reduce_mean - Pod warunkiem, że nie zostanie użyty atrybut redukcji_indeksów.
    tf.reshape
    tf.sigmoid
    tf.space_to_batch_nd - O ile tensor wejściowy ma wartość 4D (1 partia + 2 przestrzenne + 1 inna).
    tf.space_to_depth
    tf.split - Tak długo, jak num nie jest podany, a num_or_size_split zawiera liczbę podziałów jako tensor 0D.
    tf.squeeze - Dopóki oś nie jest podana.
    tf.squared_difference
    tf.strided_slice - o ile maska ​​ellipsis_mask i new_axis_mask nie są używane.
    tf.transpose - dopóki koniugat nie jest używany.

###  8
Proste konwersje, ciągłe składanie i łączenie

Wiele operacji TensorFlow może być przetwarzanych przez TensorFlow Lite, nawet jeśli nie mają bezpośredniego odpowiednika. Dotyczy to operacji, które można po prostu usunąć z grafu (tf.identity), zastąpić tensorami (tf.placeholder) lub połączyć w bardziej złożone operacje (tf.nn.bias_add). Nawet niektóre obsługiwane operacje mogą czasami zostać usunięte za pomocą jednego z tych procesów.

Oto niewyczerpująca lista operacji TensorFlow, które są zwykle usuwane z grafu:

Uwaga: Wiele z tych operacji nie ma odpowiedników TensorFlow Lite, a odpowiedni model nie będzie podlegał konwersji, jeśli nie można ich uniknąć lub połączyć.

### 9
Nieobsługiwane operacje

Operacje TensorFlow niewymienione powyżej są prawdopodobnie nieobsługiwane. W tej chwili następujące popularne operacje nie są obecnie obsługiwane:

    tf.depth_to_space

Układa dane z głębokości na bloki danych przestrzennych. To jest odwrotna transformacja SpaceToDepth. Mówiąc dokładniej, ta operacja wyświetla kopię wejściowego tensora, w którym wartości z wymiaru głębokości są przenoszone w blokach przestrzennych na wymiary wysokości i szerokości. Attr block_size wskazuje rozmiar bloku wejściowego i sposób przenoszenia danych.

### 10
Operacje TensorFlow Lite

Następujące operacje TensorFlow Lite są w pełni obsługiwane i używane zamiast wymienionych powyżej operacji TensorFlow:

### 11

Podsumowanie

