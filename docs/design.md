# 設計

## 目的と対象範囲

Mod・Plugin開発者が同じ基準データから複数のMinecraftサーバーを並行起動し、ポートを衝突させずに検証し、必要な成果を次の基準へ取り込む。
worktree管理はソース分離の手段で、ポート・プロセス・保存データの管理が中心となる。

初期対象はWindows/macOS・Python 3.12。GUIはPySide6/Qt Widgets、DBはSQLite。
利用者が用意したJavaとサーバー成果物をprofileで指定する。Minecraft/loader/Mod/Pluginのバージョンを本体で固定しない。
標準的なserver.propertiesとJVM引数、およびプロジェクト指定adapter/コマンドで接続する。実機試験には具体的なprofileと成果物hashを記録する。
Linux・SSH遠隔操作・MCP・バイナリ自動取得は初期範囲外。追加対応は別設計とする。

## 構成と責務

```text
人間CLI / GUI / Python client / JSONハーネス
                   ↓ version付きローカル管理契約
     ホスト・OSユーザー単位の単一監督プロセス
                   ↓
      タスク・worktree / 実行環境 / ポート / データ / 開発連携
                   ↓
               Git・OS・SQLite・ファイル領域
```

同一ユーザーの別管理rootも共通のポート台帳を通す。別ユーザー/管理外processはOS検査で競合を検出し、完全な協調予約の保証には含めない。
clientはDBへ直接書き込まない。GUI/CLI終了で監督・JVM・操作記録を失わない。
ownerは協調上の担当記録で、OS ACLの代替ではない。

タスクには単一変更repoのworktreeと、完全commit hashを固定したdetached依存repoを関連付ける。
任意repo/既存worktreeを明示登録でき、Issue番号・ブランチ命名・開発基準refをツール本体へ固定しない。
sourceとenvironmentのworld/runtimeデータを分離する。primaryのcheckoutや他ownerの変更を操作しない。
fetchは明示指定、commit/push/PR/merge/branch削除は本体の管理対象外。

## ポートとサービス

サービスは名前・enabled・複数endpoint・設定adapter・準備完了検査を持つ。
endpointはhost identity、TCP/UDP、address、port、v6Onlyを持ち、IPv4/IPv6 wildcardとdual-stackの重なりを判定する。
固定値は衝突時に拒否、自動値は明示範囲から割り当てる。全サービスを一括計画・予約し、部分成功を返さない。

Minecraft、RCON、Query、JDWP、Management API、その他Mod/Pluginの待受を同じ割当て契約で扱う。
RCON/Management APIは必須にしない。対応serverの設定制約に合わないbind指定は拒否する。
任意serviceは設定反映・無効化・実待受検査が接続して初めて起動確認済みとする。

「無効化」は次回起動設定の変更、「停止」は実socketの閉鎖、「解放」は管理予約の返却。
対応しないlive変更は正常停止→設定変更→再起動で反映する。
通常stopは割当て保持、一時環境は終了後返却を選べる。所有process/childの終了不明時は予約を保持する。
外部processのkill、Firewall変更、実行中の自動ポート変更はしない。

prebindでOSの空きを確認後、socketを閉じてJVMを起動し、実待受と所有processを照合する。
本bindまでのraceは外部processに対して排除できない。旧processの終了を確認した場合だけ、自動割当てを有限再選定する。
監督再起動、PID再利用、boot変更を照合する。PIDのみで所有や終了を断定しない。
正常停止はprofileで指定し、RCON無効時も所有stdin等で行う。停止方式のない構成は起動前に検出する。
一般serverのexitとMod固有データの保存証明は別に記録する。

## 基準データ・除外・独立展開

datasetの種別はworld、directory、file。source、環境内の相対配置先、取り込み可否を登録する。
immutable世代にmanifest/hash/親世代/由来/除外規則を記録し、環境は作成元世代を固定して通常コピーする。hardlinkは使わない。
配置先の重複・親子配置、管理範囲外、リンク/reparse point/特殊ファイルを拒否する。

directory配下では相対pathによる単体file、directory全体、globを除外できる。
例：`server.properties`、`logs/`、`**/*.lock`、`plugins/example/cache/`。
照合pathはPOSIX相対表記、初期版は大文字小文字を区別し、`**`は任意階層、directory末尾は配下全体を意味する。case-insensitive FS上の名前衝突は拒否する。
否定規則による再包含は初期範囲外。対象・除外を確定前にpreviewする。

取得・展開・snapshot・差分・取り込みが同じ選択集合を使う。
除外は削除要求ではなく、展開/復元で既存除外fileを消さず、取り込みで削除候補にしない。
規則は世代・環境ごとに固定し、変更による集合差分を明示する。
基準コピー後にport/秘密/環境pathを注入し、その箇所と元値をprivateに記録して取り込みから除く。

## snapshot・取り込み・基準確定

snapshotと取り込みはserverと関連writerを停止して行う。管理外writerは利用者の停止確認が必要。
登録worktreeの環境、または明示登録したworktree内datasetを取り込み元にできる。
作成時base、元の現在data、最新基準の3-way比較で追加/変更/削除をpreview・選択する。

テキストは3-wayマージ、両側binary変更は採用元を選択、worldは整合単位全体を採用する。
worldファイル/チャンクの自動合成は初期範囲外。関連Mod dataとの整合単位をprofileで定義する。
テキスト競合がなくても意味上の整合性はvalidator/実試験で確認する。

取り込みはstaging候補を作り、競合解決・独立環境での検証後に新immutable世代を明示確定する。
最新基準が候補作成時から変わったら再比較し、基準を黙って上書きしない。
新基準公開で既存環境の参照世代・dataは変えない。
worktree、environment、snapshot、基準世代の削除は別操作とする。
quota/使用量と参照保護を行い、GCは計画確認後の明示回収に限定する。

## 開発者向け機能

- 明示build profile、taskごとのoutput/cache、成果物hash、旧JAR残留/二重配置検出
- 保存停止→配備→起動→ready、保存・再起動・再読込の値照合、GameTest等のadapter
- Java/server/loader/Mod/Plugin/引数/基準世代/source状態と実行条件の記録
- runごとのlog/crash/終了codeと明示診断export、秘密redaction
- 接続先取得、RCON client、プロジェクト固有Management API adapter、writerと停止の排他
- proxy/backend等のDAG構成、全node endpointの一括計画、ready順起動・逆順停止・部分失敗保全
- 利用者指定テストclient、共有client排他、既存認証参照
- 構成/version matrix、資源/並行数上限、条件を明示した性能比較と欠測表示

JDK/server/client/worldは配布物に含めず、EULA承諾や認証設定は利用者が行う。

## 公開API・AIハーネス・GUI

将来のmcdevlabは人間表示とmachine JSON入口を持つ。
JSON stdin/stdoutにversion、operationId、input hash、結果状態を持ち、capabilities/schema/status/endpointsを取得できる。
同ID同入力は状態照合、同ID別入力は拒否、結果不明のmutationは自動再実行しない。
作用前拒否と作用後不明を区別し、選択不足は非対話errorで返す。raw secretは通常出力しない。
Python clientもこの監督契約を使用し、公開APIの副作用・例外・戻り値を文書化する。

GUIはQt Widgetsで環境/ポート/衝突、除外preview、3-way diff、候補検証/確定、build/test/診断を扱う。
重い処理をUI thread外へ置き、GUI終了をserver停止・操作取消成功とみなさない。

## 保存構造と整合性

ホスト共通台帳はendpoint予約と監督所有を管理し、root台帳は以下を管理する。

| テーブル | 責務 |
|---|---|
| repositories / tasks / task_repositories | source・owner・起点commit・worktree |
| environments / services | 実行配置・profile・サービス要求 |
| port_allocations / runs | endpoint割当て・process開始識別・実待受・停止結果 |
| operations | operation ID・入力hash・段階・結果不明と復旧 |
| datasets / dataset_versions | 種別・世代・manifest・除外と由来 |
| environment_datasets / merge_operations | 固定base・候補・競合・検証・確定先 |

データ本体はファイル領域に置く。DBの登録はGit/OS/FS実体の代替ではなく操作時に照合する。
タスク/環境のOS lockと短いDB transactionを使い、重いGit/FS/通信をDB write transaction中に実行しない。
公開前に前提世代/owner/stateを再照合し、途中失敗は記録と実体を保全して復旧待ちにする。
保存の正常完了と停電耐性を同一の保証として扱わない。

## 移植方針と完成条件

既存 .github のendpoint重なり判定、prebind、OS process所有、worktree owner/保全の考え方を利用する。
固定repo一覧・SushiEric必須API/証跡・固定3port・Query/JDWP無効固定・Maven/Gradle専用契約・旧DB互換は持ち込まない。
元workspaceに変更やdata移動を加えない。

最終受入はWindows/macOSで、並行worktree・RCON有無・任意port・基準除外・保存往復・取り込み・GUI/AI・複数server/client・matrix/性能を接続して確認する。
未実行・他OS専用・未知adapterは対応済みと報告しない。フェーズ完成条件とIssue依存はroadmapで管理する。
