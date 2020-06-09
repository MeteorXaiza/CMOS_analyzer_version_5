0. 動作環境
xaizalibs を.pyファイルが入ったディレクトリに入れてください。動作環境はxaizalibsのものと同じです。
https://github.com/MeteorXaiza/xaizalibs


1. 使い方
ターミナル上で動かしてください。
例）ターミナル =>
  --------------------------------------------
    python gen_BG_stats.py -i ./frame_20190901
  --------------------------------------------
引数に「-h」を指定すると、コマンド引数のヘルプが表示されます。
例）ターミナル =>
  ---------------------------
    python gen_BG_stats.py -h
  ---------------------------
引数はターミナル上だけでなく、configファイル(~~.ini)からも指定できます。その際は、引数に「-c [config_file_path]」と指定してください。configファイルは付属したものを参考にし適宜書き換えて使ってください。（~~_config.ini）
例）ターミナル =>
  ---------------------------------------------
  python gen_BG_stats.py -c BG_stats_config.ini
  ---------------------------------------------
また、引数はターミナル上で指定したものが優先されます。
例）
  BG_stats_config.ini =>
  --------------------------------------------------------------------
    [input]
    directory_path = ./frame_20190315/
  --------------------------------------------------------------------
  ターミナル =>
  --------------------------------------------------------------------
    python gen_BG_stats.py -c BG_stats_config.ini -i ./frame_20190913/
  --------------------------------------------------------------------
  configファイル上では、解析するディレクトリが「./frame_20190315/」に指定されていて、ターミナル上では、「./frame_20190913/」に指定されている。この場合、ターミナルの「./frame_20190913/」が優先され、解析されるディレクトリとなる。
コマンドライン上でのコマンド「python gen_BG_stats.py」などを短縮するには、「~/.bashrc」にaliasを追加するのが便利です。
例）
  .bashrc =>
  ----------------------------------------------------------------------------------------------
    alias gen_BG_stats='python /Users/MeteorXaiza/Python/CMOS_analyzer_version5/gen_BG_stats.py'
  ----------------------------------------------------------------------------------------------
  ターミナル =>
  ----------------------------------------------------------------------------------------------
    gen_BG_stats -c BG_stats_config.ini
  ----------------------------------------------------------------------------------------------


2. gen_BG_stats.py
バックグラウンド（BG）の平均値や、標準偏差、歪度、尖度、最小値、最大値、イベントの範囲にならなかったフレーム数のフレームファイルを出力します。標準偏差は不偏標準偏差（残差二乗和を(フレーム数)-1で割った分散の正の平方根）です。尖度は正規分布のものを0としたものです(μ_4/μ_2^2-3)。またBGのPHの統計情報を書かれたPH_statsファイルを出力します。

2.1 引数
--config_file, -c
  コンフィグファイルのパスを指定することで、引数を設定できます。
--input_directory, -i, (config : [input], directory_path)
  解析するフレームとなるファイルが入ったディレクトリパスを指定できます。何も指定しなければ、カレントディレクトリ「./」を指定したものとみなします。
--match_file_name, -m, (config : [input], match_file_name)
  解析するフレームファイル名を正規表現で指定します。何も指定しなければ、「.+\.fits」を指定したとみなし、ファイル名が「~~.fits」となっているものが解析に使用されます。
--frame_list_file, (config : [input], frame_list_file_path)
  解析するフレームのファイルパスが書かれたフレームリストファイルを指定できます。フレームリストファイルについては2.2 をご覧ください指定した場合、--input_directoryと--match_file_nameの指定は無視されます。「None」を指定、または、何も指定しなければ、--input_directoryと--match_file_nameの指定により解析するフレームファイルを決めます。
--limit_frame_num, (config : [input], limit_frame_num)
  解析に使用するフレーム数を指定できます。「None」を指定、または、何も指定しなければ、ファイル名が--match_file_nameでマッチする全てのフレームファイル、あるいは、フレームリストファイルのフレームファイルが解析に使用されます。
--event_list_file, (config : [input], event_list_file_path)
  イベントリストファイルのパスを指定することで、フレームの中にあるイベントを取り除いて解析できます。取り除く範囲はイベントリストのmax_leakに依存します。
  例）MAXLEAK=4 => 取り除く範囲 : 9x9ピクセル
  イベントの範囲となったピクセルのフレームは解析に含まれません。解析に含まれたフレーム数がある程度少ない場合、そのピクセルの解析結果は「nan」になります。詳細は2.3 をご覧ください。「None」を指定、または、何も指定しなければ、フレームの中にイベントはないものとみなし、全てのピクセルが解析に使用されます。
--valid_pixel, (config : [input], valid_pixel)
  PH_statsの統計情報を計算する際、有効/無効なピクセルをフィルターに掛ける際の条件式を指定できます。「かつ（and）」と「または（or）」は「*」と「+」で表現してください。条件式に使うことができる変数と記述方法は2.4 をご覧ください。
--zero_level_frame_file, (config : [input], zero_level_frame_file_path)
  バックグラウンドのPHを計算する際のzero_levelフレームファイルパスを指定できます。「None」を指定、または、何も指定しなければ、ゼロレベルフレームはBG平均値フレームとします。
--HDU_index, (config : [input], HDU_index)
  解析するフレームファイルのHDUのインデックスを指定できます。何も指定しなければ、「0」を指定したとみなし、解析します。
--zero_level_frame_file_HDU_index, (config : [input], zero_level_frame_file_HDU_index)
  --zero_level_frame_fileで指定するファイルののHDUのインデックスを指定できます。何も指定しなければ、「0」を指定したとみなし、解析します。
--valid_frame_shape, (config : [input], valid_frame_shape)
  解析するフレームのサイズ（ピクセル数）を指定できます。--input_directoryで指定したディレクトリの中にあるフレームのサイズが混在している場合、--valid_frame_shapeで指定されたサイズのフレームが解析されます。指定の仕方は「[高さ(Yの大きさ)]x[幅(Xの大きさ)]」としてください。
  例）2040x2048
  「None」を指定、または、何も指定しなければ、--match_file_nameでマッチするファイルのうち、名前順の一番先頭のファイル名のフレームのサイズを指定したとみなします（その際、一度そのファイルを読み込むことになります）。
--invalid_shape_process, (config : [input], invalid_shape_process)
  --valid_frame_shapeで指定されたサイズ以外のフレームサイズのフレームを解析しようとした際の処理を指定できます。「continue」、「quit」、「select」の3つから指定してください。何も指定しなければ、continueを指定したものとみなします。continueを指定した場合、解析せずにそのフレームを無視します。quitを指定した場合、以降の解析も行わずに解析を完全に終了し、何も出力されません。selectを指定した場合、以降に解析するフレームサイズをこれまでのものと同じにするか、今回の違うフレームサイズにするかを選択できます。
--mean_BG_frame_filee, -o, (config : [output], mean_BG_frame_file_path)
  出力するバックグラウンドの平均値（BG平均）のフレームのファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、ファイルは出力されません。
--std_BG_frame_file, (config : [output], std_BG_frame_file_path)
  出力するバックグラウンドの標準偏差のフレーム（BG標準偏差）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、ファイルは出力されません。
--skewness_BG_frame_file, (config : [output], skewness_BG_frame_file_path)
  出力するバックグラウンドの歪度のフレーム（BG歪度）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、ファイルは出力されません。
--kurtosis_BG_frame_file, (config : [output], kurtosis_BG_frame_file_path)
  出力するバックグラウンドの尖度のフレーム（BG尖度）のファイルのパスを指定できます。拡張子は「.fits」にしてください。標準偏差が0のピクセルは、尖度の解析結果がnanになります。「None」を指定、または、何も指定しなければ、ファイルは出力されません。
--min_BG_frame_file, (config : [output], min_BG_frame_file_path)
  出力するバックグラウンドの最小値のフレーム（BG最小値）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、ファイルは出力されません。
--max_BG_frame_file, (config : [output], max_BG_frame_file_path)
  出力するバックグラウンドの最大値のフレーム（BG最大値）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、バックグラウンドの最大値のフレームのファイルは出力されません。
--cnt_BG_frame_file, (config : [output], cnt_BG_frame_file_path)
  イベントの範囲にならなかったピクセルのフレーム数のフレーム（BGフレーム数）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、ファイルは出力されません。
--PH_stats_file, (config : [output], PH_stats_file_path)
  またBGのPHの統計情報を書かれたPH_statsファイルのパスを指定できます。PH_statsファイルについては2.2.2 をご覧ください拡張子は「.json」にしてください。「None」を指定、または、何も指定しなければ、ファイルは出力されません。

2.2 詳細
2.2.1 フレームリストファイル
フレームファイルのファイルパスを記述し、改行で区切ったテキストファイル。
例）フレームリストファイル =>
  -------------------------------------------------------------------
  /Users/Documents/GSENSE6060BSI/BG_20200608_roomT_int_0.049ms_0.fits
  /Users/Documents/GSENSE6060BSI/BG_20200608_roomT_int_0.049ms_1.fits
  /Users/Documents/GSENSE6060BSI/BG_20200608_roomT_int_0.049ms_2.fits
  /Users/Documents/GSENSE6060BSI/BG_20200608_roomT_int_0.049ms_3.fits
  /Users/Documents/GSENSE6060BSI/BG_20200608_roomT_int_0.049ms_4.fits
  /Users/Documents/GSENSE6060BSI/BG_20200608_roomT_int_0.049ms_5.fits
  -------------------------------------------------------------------
  ファイル名 : frame_list_BG_20200608_roomT_int_0.049ms.txt

2.2.2 PH_statsファイル
PH（=(元の信号値)-(zero_levelの信号値)）の統計情報（平均値、標準偏差、歪度、尖度、最小値、最大値、サンプルサイズ）が書かれたJSONファイルです。

2.3 解析に必要なフレーム数
平均値 => 1フレーム以上
標準偏差 => 2フレーム以上
歪度 => 2フレーム以上
尖度 => 2フレーム以上
最小値 => 1フレーム以上
最大値 => 1フレーム以上
フレームカウント => 0フレーム以上

2.4 valid_pixelの変数と記述方法
2.4.1 変数
Y => フレームのY（column_address）
X => フレームのX（row_address）
mean => フレームのBG平均値（--mean_BG_frame_file_path　で保存されるフレーム）
std => フレームのBG標準偏差（--std_BG_frame_file_path　で保存されるフレーム）
skewness => フレームのBG歪度（--skewness_BG_frame_file_path　で保存されるフレーム）
kurtosis => フレームのBG尖度（--kurtosis_BG_frame_file_path　で保存されるフレーム）
min => フレームのBG最小値（--min_BG_frame_file_path　で保存されるフレーム）
max => フレームのBG最大値（--max_BG_frame_file_path　で保存されるフレーム）
cnt => フレームカウント（--cnt_BG_frame_file_path　で保存されるフレーム）

2.4.2 記述方法
BG平均値が1000未満かつBG標準偏差が50未満のピクセルを指定する場合 =>
(mean<1000)*(std<50)


3. gen_event_list.py
フレーム中のイベントを抽出し、イベントのデータ（フレーム、イベントの中心のピクセル、PHasum、vortex、PH、appendix）をまとめたイベントリストファイルを出力します。

3.1 引数
--config_file, -c
  gen_BG_stats.pyのものと同様です。
--input_directory, -i, (config : [input], directory_path)
    gen_BG_stats.pyのものと同様です。
--match_file_name, -m, (config : [input], match_file_name)
    gen_BG_stats.pyのものと同様です。
--frame_list_file, (config : [input], frame_list_file_path)
    gen_BG_stats.pyのものと同様です。
--limit_frame_num, (config : [input], limit_frame_num)
  gen_BG_stats.pyのものと同様です。
--zero_level_frame_file, (config : [input], zero_level_frame_file_path)
  PHを計算する際のzero_levelフレームファイルパスを指定できます。
--threshold_file, -th, (config : [input], threshold_file_path)
  イベント抽出のパラメータとしてのthresholdファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、--event_thと--split_thで指定された値で解析を行います。
--event_th, -eth, (config : [input], event_th)
  event_thを指定できます。「None」を指定、または、何も指定しなければ、--threshold_fileで指定されたパスのファイルを参照し、解析に用います。
--split_th, -sth, (config : [input], split_th)
  split_thを指定できます。「None」を指定、または、何も指定しなければ、--threshold_fileで指定されたパスのファイルを参照し、解析に用います。
--max_leak, -ml, (config : [input], max_leak)
  max_leakを指定できます。何も指定しなければ、「1」を指定したとみなします。
--appendix_frame_list_file, -a, (config : [input], appendix_frame_list_file_path)
  appendixフレームリストファイルのパスを指定できます。appendixフレームリストファイルについては3.2 をご覧ください。「None」を指定、または、何も指定しなければ、出力されるイベントリストにappendixは付属しません。
--HDU_index, (config : [input], HDU_index)
  gen_BG_stats.pyのものと同様です。
--zero_level_frame_file_HDU_index, (config : [input], zero_level_frame_file_HDU_index)
  gen_BG_stats.pyのものと同様です。
--invalid_shape_process, (config : [input], invalid_shape_process)
  --zero_level_frame_fileで指定されたサイズ以外のフレームサイズのフレームを解析しようとした際の処理を指定できます。「continue」、「quit」の2つから指定してください。何も指定しなければ、continueを指定したものとみなします。continueを指定した場合、解析せずにそのフレームを無視します。quitを指定した場合、以降の解析も行わずに解析を完全に終了し、何も出力されません。
--event_list_file, -o, (continue : [output], event_list_file_path)
  解析した結果を出力するイベントリストファイルのパスを指定できます。イベントリストファイルについては3.2 をご覧ください。

3.2 詳細
3.2.1 appendixフレームリストファイル
イベントリストのappendixとして付属させるフレームのファイルパスを記述し、改行で区切ったテキストファイル
例）appendixフレームリストファイル =>
  ------------------------------------------------------------------------
  ./mean_BG_frame/mean_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ./std_BG_frame/std_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ./skewness_BG_frame/skewness_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ./kurtosis_BG_frame/kurtosis_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ./min_BG_frame/min_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ./max_BG_frame/max_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ./cnt_BG_frame/cnt_BG_frame_BG_20200608_roomT_int_0.049ms.fits
  ------------------------------------------------------------------------
  ファイル名 : BG_stats_frame_list.txt

3.2.2 イベントリストファイル
イベントのデータをまとめた2次元配列のFITSファイル。1行ごとに1つのイベントのデータを格納している。（N=(2*max_leak+1)**2とする）
0列目 : フレーム番号
1列目 : イベントの中心となったピクセルのY（column_address）
2列目 : イベントの中心となったピクセルのX（row_address）
3列目 : イベントを抽出したときのmax_leak
4列目 : PHasum
5列目 : vortex
6列目 : PH[0]
7列目 : PH[1]
.
.
.
N+5列目 : PH[N-1]
N+6列目 : appendix[0][0]
N+7列目 : appendix[0][1]
2*N+5列目 : appendix[0][N-1]
2*N+6列目 : appendix[1][0]
2*N+7列目 : appendix[1][1]
.
.
.
3*N+5列目 : appendix[1][N-1]
3*N+6列目 : appendix[2][0]
.
.
.

4. gen_frame_stats.py
任意の関数のフレームの統計情報を記述したframe_statsファイルを出力します。

4.1 引数
