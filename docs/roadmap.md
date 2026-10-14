# フェーズ別計画

マイルストーンは機能が成立する段階ごとに分ける。Issueは実装・呼出し元・検証・文書を含む一成果として扱う。
後続の変更は依存Issueの確定commitを待つ。独立Issueのみ共有契約・port・実機・出力先の競合を確認して並行化できる。

## フェーズ0：独立リポジトリとビルド基盤

Python 3.12の独立パッケージをWindows/macOSでビルド・インストールでき、GUI依存なしでimportできる。設計・Issue依存・CIが揃う。機能実装・リリースはこのフェーズに含めない。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#1](https://github.com/rs0325/minecraft-dev-lab/issues/1) | build: 独立パッケージとビルドCIを初期構築する | なし |

## フェーズ1：ポート衝突を防ぐ並行サーバー環境

2つ以上のworktreeに対応する独立Minecraft環境を同時起動し、必要な任意TCP/UDPポートの割当て・実待受照合・正常停止・解放を確認する。片方だけRCONを無効化でき、監督再起動・衝突・停止不明で予約を誤解放しない。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#2](https://github.com/rs0325/minecraft-dev-lab/issues/2) | feat: 管理root・環境状態・公開操作契約を定義する | #1 |
| [#3](https://github.com/rs0325/minecraft-dev-lab/issues/3) | feat: 任意リポジトリのworktreeとタスクを管理する | #2 |
| [#4](https://github.com/rs0325/minecraft-dev-lab/issues/4) | feat: 任意TCP・UDPポートを一括割当てして衝突を診断する | #2 |
| [#5](https://github.com/rs0325/minecraft-dev-lab/issues/5) | feat: Minecraftと任意サービスのポート設定を環境へ反映する | #4 |
| [#6](https://github.com/rs0325/minecraft-dev-lab/issues/6) | feat: サーバー起動・準備完了・正常停止とプロセス所有を監督する | #2, #4, #5 |
| [#7](https://github.com/rs0325/minecraft-dev-lab/issues/7) | feat: CLIからサービス無効化・ポート解放・環境復旧を操作する | #3, #6 |

## フェーズ2：基準データ・除外・マージ

ワールド・任意ディレクトリ・単体ファイルを世代化し、除外規則付きで環境へ展開する。任意登録worktree由来のデータを3-way比較・候補検証・明示確定で新基準へ取り込める。競合・除外・稼働中データを保全する。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#8](https://github.com/rs0325/minecraft-dev-lab/issues/8) | feat: ワールド・ディレクトリ・単体ファイルと除外規則を登録する | #2, #7 |
| [#9](https://github.com/rs0325/minecraft-dev-lab/issues/9) | feat: 基準データを世代化して環境へ独立展開する | #8, #5 |
| [#10](https://github.com/rs0325/minecraft-dev-lab/issues/10) | feat: 停止データのsnapshot・基準復元と環境データ保全を提供する | #9, #6 |
| [#11](https://github.com/rs0325/minecraft-dev-lab/issues/11) | feat: 任意worktree由来データを3-way比較して取り込み候補を作る | #9, #10 |
| [#12](https://github.com/rs0325/minecraft-dev-lab/issues/12) | feat: 候補データの検証・基準確定と参照保護付き回収を提供する | #11 |

## フェーズ3：Mod・Plugin開発とAIハーネス

ビルド・配備・保存再起動試験・診断を実行条件と紐づける。CLI・公開Python API・JSONハーネスから同じ管理契約を利用でき、操作IDによる照合と秘密保護が成立する。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#13](https://github.com/rs0325/minecraft-dev-lab/issues/13) | feat: ビルドprofileと実行条件・成果物hashを固定する | #7, #9 |
| [#14](https://github.com/rs0325/minecraft-dev-lab/issues/14) | feat: 成果物配備と保存停止からの正常再起動を一括実行する | #13, #10 |
| [#15](https://github.com/rs0325/minecraft-dev-lab/issues/15) | feat: RCON・Management APIと任意サービス接続を分離して提供する | #6, #5 |
| [#16](https://github.com/rs0325/minecraft-dev-lab/issues/16) | feat: 任意検証と保存・再起動・再読込試験を実行する | #14, #15, #12 |
| [#17](https://github.com/rs0325/minecraft-dev-lab/issues/17) | feat: run単位のログ・障害情報と操作結果を収集する | #6, #13, #16 |
| [#18](https://github.com/rs0325/minecraft-dev-lab/issues/18) | feat: 公開Python APIとJSON AIハーネスの操作契約を提供する | #7, #12, #16, #17 |

## フェーズ4：GUIによる環境・データ・開発操作

PySide6/Qt WidgetsのGUIから共通管理APIを利用し、並行環境・ポート・データ差分と取り込み・開発試験を操作できる。GUI終了で監督・サーバー・操作記録を失わない。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#19](https://github.com/rs0325/minecraft-dev-lab/issues/19) | feat: GUIでタスク・サーバー・ポートを操作する | #18 |
| [#20](https://github.com/rs0325/minecraft-dev-lab/issues/20) | feat: GUIでデータ除外・取り込みと開発試験を操作する | #19 |

## フェーズ5：複数サーバー構成・クライアント・比較計測

プロキシを含む複数サーバー構成、明示テストクライアント、バージョン/構成マトリクス、性能比較を独立データ・競合しないポートで実行できる。共有資源と部分失敗を保全する。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#21](https://github.com/rs0325/minecraft-dev-lab/issues/21) | feat: プロキシを含む複数サーバー構成を起動管理する | #18, #13 |
| [#22](https://github.com/rs0325/minecraft-dev-lab/issues/22) | feat: 指定テストクライアントを環境に接続して検証結果を記録する | #21, #16 |
| [#23](https://github.com/rs0325/minecraft-dev-lab/issues/23) | feat: サーバー・Java・導入構成の比較試験を一括作成する | #18, #13, #16 |
| [#24](https://github.com/rs0325/minecraft-dev-lab/issues/24) | feat: 性能計測をrunへ保存して条件付きで比較する | #23, #17 |

## フェーズ6：配布と総合受入

CLI/ライブラリ/AIハーネスとWindows/macOSのGUI配布物を用意し、クリーン環境で導入から並行検証・マージ・復旧まで受入確認する。OS別の結果・未対応機能を明示し、利用文書が実装と一致する。公開リリースは別途許可を要する。

| Issue | 成果 | 前提Issue |
|---|---|---|
| [#25](https://github.com/rs0325/minecraft-dev-lab/issues/25) | build: CLI・ライブラリとOS別GUI配布物を構築する | #20, #21, #22, #24 |
| [#26](https://github.com/rs0325/minecraft-dev-lab/issues/26) | test: 並行開発・基準マージ・障害復旧をOS別に総合受入する | #25 |
| [#27](https://github.com/rs0325/minecraft-dev-lab/issues/27) | docs: 導入・公開API・AI操作と復旧手順を完成させる | #26 |

## 現在の範囲

今回の公開はフェーズ0の初期ビルド基盤まで。フェーズ1以降の機能は未実装。
Issueは公開だけでcloseせず、必須検証・レビューと権限を確認して管理する。
priority/typeの専用ラベルは未作成のため本文に記載し、機能Issueには既存enhancement、文書Issueには既存documentationを使用する。
優先度はlow：新規ツールの機能整備であり、既存主要機能の障害ではない。
