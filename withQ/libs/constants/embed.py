import discord

embed = discord.Embed(
    title="withQの使い方",
    description='withQ は、Discord でゲームをする複数の友人に対して一緒にゲームをプレイする機会を提供するボットです。\n'
    'withQ の使用方法は、以下のとおりです。\n'
    '\n'
    '**コマンドの入力方法**\n'
    '```/w [タイトル] [募集人数] [締め切り時間] [メンション] [参加者通知設定]```\n'
    '\n'
    '**各値について**\n'
    '\n'
    '※必須値は必ず上記のコマンド順で入力してください。オプション値は順不問となり、設定されていなくても問題ありません。\n'
    '※[締め切り時間]の値が設定されていない場合、6時間後に自動で募集が取り消されます。\n'
    '\n'
    '**[タイトル]**・・・必須値。募集したい内容やタイトルを入力します\n'
    '\n'
    '**[募集人数]**・・・必須値。募集したい人数を入力します。募集人数に達したときに募集を終了して参加者をメンションします\n'
    '\n'
    '**[締め切り時間]**・・・オプション値。募集に締め切り時間を設定したい場合に利用できます。値が設定されていない場合、6時間後に募集が取り消されます\n'
    '\n'
    '有効な値は以下の通りです。\n'
    'コマンドの値・・・機能\n'
    'hh:mm・・・入力された時間に募集を締め切ります。\n'
    'mm/dd/hh:mm・・・入力された日付と時間に募集を締め切ります。  \n'
    'yyyy/mm/dd/hh:mm・・・入力された年月日と時間に募集を締め切ります。\n'
    '\n'
    '**[メンション]**・・・オプション値。botが送信する募集メッセージに @everyone または @here のメンションを追加したい場合に利用できます\n'
    '\n'
    '有効な値は以下の通りです。\n'
    'コマンドの値・・・機能\n'
    'e・・・募集メッセージに @everyone を付与します。\n'
    'h・・・募集メッセージに @here を付与します。\n'
    '\n'
    '**[参加者通知設定]**・・・オプション。参加者通知設定コマンドがある場合に募集者に送信される参加通知DMと参加取り消し通知DMを送信しないようにできます\n'
    '\n'
    '有効な値は以下の通りです。\n'
    'コマンドの値・・・機能\n'
    'n・・・参加通知DMと参加取り消しDMを無効にします。\n'
    '\n'
    '**募集メッセージの各ボタンについて**\n'
    '\n'
    'コマンドによって withQ が送信する募集メッセージには IN Qボタン、DE Qボタン、〆ボタン、CANCELボタンの4種類のボタンが存在します。\n'
    '\n'
    '各ボタンの機能については以下の通りです。\n'
    'ボタン名・・・機能\n'
    'IN Q・・・押下することで募集に参加することができます。\n'
    'DE Q・・・すでに対象の募集に参加している場合、押下することで募集を取り消すことができます。\n'
    '〆・・・募集者のみが押下することができます。押下時点で募集を締め切り、参加者をメンションします。\n'
    'CANCEL・・・募集者のみが押下することができます。押下することで募集を終了することができます。\n'
    '\n'
    '\n'
    'withQ ver 1.0.0'
)