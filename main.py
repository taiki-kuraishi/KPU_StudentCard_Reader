import nfc


def on_connect(tag: nfc.tag.Tag) -> bool:
    print("connected")
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            print("\n".join(tag.dump()))  # タグの全情報を表示
        except nfc.tag.tt3.Type3TagCommandError:
            print("Type3TagCommandError occurred")
    # elif isinstance(tag, nfc.tag.tt2.Type2Tag):
    #     print(tag.identifier)  # タグの識別子を表示
    # elif isinstance(tag, nfc.tag.tt4.Type4Tag):
    #     print(tag.product)  # タグの製品名を表示
    # 他のタグタイプに対する処理...
    return True


def on_release(tag: nfc.tag.Tag) -> None:
    print("released")


with nfc.ContactlessFrontend("usb") as clf:
    while True:
        clf.connect(rdwr={"on-connect": on_connect, "on-release": on_release})
