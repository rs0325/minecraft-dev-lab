# ビルドと検証

## 対応範囲

Python 3.12専用の初期パッケージ。Hatchlingでwheel/sdistを生成する。
現在はpackage markerと設計/ビルド基盤のみで、サーバー制御・CLI・GUI・公開管理APIは未実装。
GUI依存はgui extra、開発時のbuild/ruffはdev extraに分離する。
pyproject.tomlで直接依存の版を固定する。推移依存や全実行環境まで固定した再現性は後続Issueで扱う。

## Windows

```powershell
python3.12 -m venv .venv
.venv/Scripts/python -m pip install ".[dev]"
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m build
.venv/Scripts/python scripts/check_distribution.py
```

## macOS

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install ".[dev]"
.venv/bin/python -m ruff check .
.venv/bin/python -m build
.venv/bin/python scripts/check_distribution.py
```

check_distribution.pyはdist内のwheelとsdistを検査し、一時venvへwheelを依存なしでインストールしてimport/metadataを確認する。
さらにsdistを展開してwheelを再構築する。networkはPEP 517 build isolationのビルド依存取得時に必要。
作業sourceからのimportで導入確認を代替しない。一時領域はスクリプトが作成した範囲だけ処理し、利用者dataを触らない。
Qtが基本依存に入っていないこと、packageとpy.typed、sdistの設計/ビルド材料があることも確認する。

## CI

GitHub ActionsでWindows/macOS・Python 3.12の同じチェックを行う。
公式checkout/setup-pythonをcommit SHAに固定し、contents権限はreadのみ。
手動dispatchも提供する。パッケージ公開・release・server起動・SSH操作は行わない。
機能テストや実Minecraft受入はまだ存在せず、ビルド成功を機能実装の完了と扱わない。

出典：[Hatchビルド設定](https://hatch.pypa.io/latest/config/build/)、[Qt for Python](https://doc.qt.io/qtforpython-6/)。
