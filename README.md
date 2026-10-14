# Minecraft Dev Lab

MinecraftのMod・Plugin開発用に、worktreeごとのサーバー・ポート・ワールド・任意データを分離し、並行検証と基準データへの取り込みを管理するツールです。

**現在は設計とビルド基盤のみです。** CLI・GUI・ライブラリの管理API・AIハーネスは未実装です。初期パッケージをimportできることは、サーバー制御や保存保証の証明ではありません。

## 計画する機能

- 任意TCP/UDPサービスのポート衝突回避、RCON等の無効化、停止確認後の割当て解除
- 任意repoのworktreeと固定commitの依存ソース、担当引継ぎ
- ワールド、任意ディレクトリ、単体ファイルの基準世代と独立した実行データ
- 除外規則、snapshot、3-way差分、取り込み候補の検証と新基準の確定
- ビルド・配備・正常再起動、保存/再読込試験、診断、JSON AIハーネス
- GUI、複数サーバー/プロキシ、テストクライアント、構成比較、性能計測

詳細は[設計](docs/design.md)と[フェーズ別計画](docs/roadmap.md)を参照してください。
[Issue一覧](https://github.com/rs0325/minecraft-dev-lab/issues)と[マイルストーン](https://github.com/rs0325/minecraft-dev-lab/milestones)で管理します。

## 開発環境とビルド

初期対象はWindows/macOS、Python 3.12です。Gitはworktree機能実装時に使用します。
管理対象のJava・サーバー・Mod/Plugin・クライアントは利用者指定で、パッケージには同梱しません。

ビルド手順と検証範囲は[ビルドガイド](docs/build.md)にあります。
GUI依存は `gui` extraに分離し、CLI・ライブラリ・ハーネスだけの利用ではQtを必要としません。

```sh
python -m pip install ".[dev]"
python -m ruff check .
python -m build
python scripts/check_distribution.py
```

将来のCLI名は `mcdevlab`、Pythonパッケージ名は `minecraft_dev_lab` です。未実装のコマンドは登録していません。

## 開発ブランチ

`develop`を開発基準、`main`をリリース用とします。初期公開はdevelopのみで、mainとリリースは未作成です。
変更Issueは `feature/issue-<番号>` の専用作業先で実装し、develop宛てに公開準備します。

Minecraft公式の製品ではありません。現時点では利用許諾ライセンスを未設定です。公開リポジトリであることを再配布許諾と扱わないでください。
