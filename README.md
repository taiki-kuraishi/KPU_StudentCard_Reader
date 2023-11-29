# はじめに
開志専門職大学の学生証を、nfcpyを使用して氏名と学籍番号を読み取るプログラムを作成しました。


# NFCリーダー
- RC-S380/S
- 対応OS : win10,win11

https://www.sony.co.jp/Products/felica/business/products/reader/RC-S380.html

# 環境構築
1. Zadigのダウンロード

    - https://zadig.akeo.ie/ 
    <br>

1. Zadigを使用して、ドライバーの置換
    - optionからList All Devicesを選択し、riverをWinUSBに変更後Replace Driverをクリック
    <br>

1. libusbの導入
    - https://libusb.info/
    - DownloadsからLatest Windows Binariesをクリックすることでダウンロードすることができる
    - `VS2015-x64\dll\libusb-1.0.dll`を`C:\Windows\System32`に配置
    - `VS2015-Win32\dll\libusb-1.0.dll`を`C:\Windows\SysWOW64`に配置
    <br>

4. nfcpyのインストール
    ```bash
    pip install nfcpy
    ```

# python環境
- python 3.11.6
- requirements.txt
    ```text
    libusb1==3.1.0
    ndeflib==0.3.3
    nfcpy==1.0.4
    pyDes==2.0.1
    pyserial==3.5
    ```

# 学生証を読み取る
- NFCを読み取り、表示するプログラム
    ```python:nfc_dump.py
    import nfc
    
    
    def on_connect(tag: nfc.tag.Tag) -> None:
        print("\n".join(tag.dump()))
    
    
    with nfc.ContactlessFrontend("usb") as clf:
        clf.connect(rdwr={"on-connect": on_connect})
    ```
    <br>

- 出力
    ```text:nfc_dump.pyの出力
    System 809E (unknown)
    Area 0000--FFFE
      Area 1000--11FF
        Random Service 64: write with key & read with key (0x1008 0x100A)
        Area 1200--12FF
        Random Service 72: write with key & read with key (0x1208 0x120A)
        Cyclic Service 72: write with key & read with key (0x120C 0x120E)
        Purse Service 72: direct with key & cashback with key & decrement with key & read with key (0x1210 0x1212 0x1214 0x1216)
        Random Service 73: write with key & read with key (0x1248 0x124A)
        Random Service 74: write with key & read with key (0x1288 0x128A)
        Random Service 700: write with key & read w/o key (0xAF08 0xAF0B)
         0000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
        Random Service 701: write w/o key (0xAF49)
         0000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
         *     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
         002D: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
    System FE00 (Common Area)
    Area 0000--FFFE
      Area 1A80--1AFF
        Area 1A81--1AFF
          Random Service 106: write with key & read w/o key (0x1A88 0x1A8B)
           0000: XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX |XXXXXXXXXXXXXXXX|
           0001: 83 4e 83 89 83 43 83 56 81 40 83 5e 83 43 83 4c |.N...C.V.@.^.C.L|
           0002: 31 35 30 31 32 33 39 34 32 30 32 32 30 34 30 31 |1501239420220401|
           0003: 32 30 32 36 30 33 33 31 41 48 32 38 30 33 33 39 |20260331AH280339|
          Area 1B00--1B3F
          Area 1B01--1B3F
            Random Service 108: write with key & read with key (0x1B08 0x1B0A)
            Area 1B40--1B7F
            Area 1B41--1B7F
              Random Service 109: write with key & read with key (0x1B48 0x1B4A)
              Area 42C0--42FF
              Area 42C1--42FF
                Random Service 267: write with key & read with key (0x42C8 0x42CA)
                Area 4300--433F
                Area 4301--433F
                  Random Service 268: write with key & read with key (0x4308 0x430A)
                  Area 4340--437F
                  Area 4341--437F
                    Random Service 269: write with key & read w/o key (0x4348 0x434B)
                     0000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
                     *     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
                     0002: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
                    Area 7A00--7A3F
                    Area 7A01--7A3F
                      Random Service 488: write with key & read with key & read w/o key (0x7A08 0x7A0A 0x7A0B)
                       0000: 33 39 32 31 30 31 30 30 31 30 36 37 35 39 34 39 |3921010010675949|
                      Area 7A40--7A7F
                      Area 7A41--7A7F
                        Random Service 489: write w/o key & read w/o key (0x7A49 0x7A4B)
                         0000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
                         *     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
                         000B: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|
    ```
    - ※学籍番号の部分はXXに変更
    <br>
- ダンプされたデータをみると以下の箇所に目当てのデータが格納されていそうです
    ```text
    Random Service 106: write with key & read w/o key (0x1A88 0x1A8B)
        0000: XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX |XXXXXXXXXXXXXXXX|
        0001: 83 4e 83 89 83 43 83 56 81 40 83 5e 83 43 83 4c |.N...C.V.@.^.C.L|
        0002: 31 35 30 31 32 33 39 34 32 30 32 32 30 34 30 31 |1501239420220401|
        0003: 32 30 32 36 30 33 33 31 41 48 32 38 30 33 33 39 |20260331AH280339|
    ```
    - ※学籍番号の部分はXXに変更

# NFCの構造
- **`write with key & read with key & read w/o key`**
    - ダンプされたデータを見るとところどころに英単語が見受けられます
    
    |       操作       |                            説明                            |
    | :--------------: | :--------------------------------------------------------: |
    | `write with key` |               鍵を使用して書き込むことが可能               |
    | `read with key`  |               鍵を使用して読み込むことが可能               |
    |  `read w/o key`  | データを読み取るために暗号鍵は不要で、鍵なしでアクセス可能 |
    <br>


- NFCに格納されたデータをプログラムで読み込むためには、以下を指定する必要があります。
    - システムコード 
    - サービスコード 
    - ブロックコード
    <br>
- 目当てのデータを読み込む場合
    - システムコード : `0xFE00`
        ```text
        System FE00 (Common Area)
        ```
    - サービスコード : `0x1A8B`
        ```text
        Random Service 106: write with key & read w/o key (0x1A88 0x1A8B)
        ```
        - 今回は、`read w/o key`を使用して読み取るので、`0x1A8B`を使用します
    - ブロックコード : `0`,`1`,`2`,`3`
        ```text
        0000: XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX |XXXXXXXXXXXXXXXX|
        0001: 83 4e 83 89 83 43 83 56 81 40 83 5e 83 43 83 4c |.N...C.V.@.^.C.L|
        0002: 31 35 30 31 32 33 39 34 32 30 32 32 30 34 30 31 |1501239420220401|
        0003: 32 30 32 36 30 33 33 31 41 48 32 38 30 33 33 39 |20260331AH280339|
        ```

# 氏名と学籍番号を抜き出す
- 氏名と学籍番号を抜き出すプログラム
    ```python:extract_student_info.py
    import nfc
    from typing import cast
    
    def on_connect(tag):
        sys_code = 0xFE00
        service_code = 0x1A8B
        idm, pmm = tag.polling(system_code=sys_code)
        tag.idm, tag.pmm, tag.sys = idm, pmm, sys_code
        sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3F)
    
        # student_num
        bc = nfc.tag.tt3.BlockCode(0, service=0)
        student_num = cast(bytearray, tag.read_without_encryption([sc], [bc]))
        student_num = student_num.decode("shift_jis")
        print("student number : " + str(student_num))
    
        # name
        bc = nfc.tag.tt3.BlockCode(1, service=0)
        name = cast(bytearray, tag.read_without_encryption([sc], [bc]))
        name = name.decode("shift_jis")
        print("name : " + str(name))
    
    
    with nfc.ContactlessFrontend("usb") as clf:
        clf.connect(rdwr={"on-connect": on_connect})
    ```
    <br>
- 出力
    ```text:extract_student_info.pyの出力
    student number : 20122XXX
    name : クライシ　タイキ
    ```
    - ※学籍番号の部分はXXに変更
    - 学籍番号と氏名（カタカナ)が出力されました。
    <br>

- プログラムの説明
    - `on_connect`関数
        - NFCタグが接続された時に呼び出されます
    - システムコードとサービスコードの指定
        ```python
        sys_code = 0xFE00
        service_code = 0x1A8B
        ```
    - システムコードの切り替え
        - 複数のシステムコードを持つ場合は、`polling`を使用してシステムコードを切り替えます。
        - 
        ```python
        idm, pmm = tag.polling(system_code=sys_code)
        tag.idm, tag.pmm, tag.sys = idm, pmm, sys_code
        ```
    - データの読み取り後、`bytearray`型に変換
        ```python
        student_num = cast(bytearray, tag.read_without_encryption([sc], [bc]))
        ```
    - デコード
        - このNFCは、`shift_jis`でエンコードされていました
        ```python
        student_num = student_num.decode("shift_jis")
        ```

# まとめ
- 学籍番号と氏名は以下のアドレスに格納されています。開専門職大学の学生証を使う方に参考になるとうれしいです。
    - 学籍番号
        - システムコード : 0xFE00
        - サービスコード : 0x1A8B
        - ブロックコード : 0
    - 氏名(カタカナ)
        - システムコード : 0xFE00
        - サービスコード : 0x1A8B
        - ブロックコード : 1
        <br>
- ブロックコード2,3には、入学年月日と卒業予定年月日が格納されていましたが、今回の目当てではないので省略させていただきました。
- これを使って、入退室の管理システムを作れたらいいなと思います。

https://github.com/taiki-kuraishi/KPU_StudentCard_Reader

# 参考文献

[nfcpy公式ドキュメント](https://nfcpy.readthedocs.io/en/latest/topics/get-started.html)
[NFCリーダー+Python+nfcpyで学生証の情報を読み取る](https://zenn.dev/3w36zj6/articles/d3894e83cb7423
)
[nfcpy で複数の System Code を持つ NFC タグを扱う方法](https://uchan.hateblo.jp/entry/2016/11/18/190237
)
