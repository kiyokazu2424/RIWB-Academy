# データベース仕様書

## 各テーブルについて

- 学生情報(user)  
  - 用途：学生ログイン管理、企業とのマッチング、自己分析など管理
  - 備考：

- 企業情報(user)  
  - 用途：企業ログイン管理、学生とのマッチング
  - 備考：サイト内で広告を打ちたいとき、広告テーブルも作り管理？

- 教材、動画(contents)  
  - 用途：学習画面で表示する動画や情報の管理
  - 備考：動画ごとにカテゴリとかつけておくとわかりやすい？→今後教材種類を増やすなら検索機能とか

- 教材、動画ジャンル(contents)  
  - 用途：教材のカテゴリやハッシュタグ管理
  - 備考：動画ごとにカテゴリとかつけておくとわかりやすい？→今後教材種類を増やすなら検索機能とか

- 教材、動画コメント(contents)  
  - 用途：各動画に対するコメント管理
  - 備考：コメントに対するリプとかどうするか

- 情報共有ルーム(chat-room,1toN)  
  - 用途：学生同士が自由に勉強のことなどを発信し合えるチャットのルーム
  - 備考：チャットルームは必要？ルーム管理はriwbがしてもいいかも

- 情報共有メッセージ(chat-message,1toN)  
  - 用途：学生同士が自由に勉強のことなどを発信し合えるチャットのメッセージ
  - 備考：質問などは流れがちなのであくまで情報発信用、チャットルームは必要？  情報共有でも話したいジャンルとかで分けてもいいかも

- 質問スレッド(chat-room,1toN)  
  - 用途：動画などの質問
  - 備考：動画の質問メイン

- 質問メッセージ(chat-message,1toN)  
  - 用途：質問スレッドに対するメッセージ
  - 備考：

- 学生と企業のチャットルーム(chat-room,1to1)  
  - 用途：就職情報やスカウトのルーム
  - 備考：スカウト回数などに制限を設けるか

- 学生と企業間のメッセージ(chat-message,1to1)  
  - 用途：就職情報やスカウトのメッセージ
  - 備考：スカウト回数などに制限を設けるか

- 1on1ルーム(chat-room,1to1)  
  - 用途：riwbメンバーとのルーム
  - 備考：ここでは学習に対する質問などはしない

- 1on1メッセージ(chat-message,1to1)  
  - 用途：riwbメンバーとの連絡
  - 備考：ここでは学習に対する質問などはしない、riwbメンバーもstaffとして一般ユーザー同様にアカウント作成？

## 各テーブルカラム表(コメントやチャット情報管理、制限字数などは要検討)

### user系

#### 学生情報(user)(エニアグラムなどは一旦保留)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| email | varchar | NO | UNI | NULL |  |
| password | varchar | NO |  | NULL |  |
| first_name | varchar | NO |  | NULL |  |
| lase_name | varchar | NO |  | NULL |  |
| phone_num | int | YES |  | NULL | for_second_auth for_find_work|
| school | char | NO |  | NULL |  |
| faculty | char | NO |  | NULL |  |
| department | char | NO |  | NULL |  |
| school_year | char | NO |  | NULL |  |
| birthday_year | int | YES |  | NULL | for_find_work |
| birthday_month | int | YES |  | NULL | for_find_work |
| birthday_day | int | YES |  | NULL | for_find_work |
| country_citizenship | varchar | YES |  | NULL | for_find_work |
| japanese_skill | int | YES |  | NULL | for_find_work |
| appeal_point | varchar | YES |  | NULL | for_find_work |
| is_superuser | varchar | NO |  | False | for_maintenance |

#### 企業情報(company)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL |  |
| email | varchar | NO | UNI | NULL |  |
| password | varchar | NO |  | NULL |  |
| company_name | varchar | NO |  | NULL |  |
| staff_name | varchar | NO |  | NULL | for_scout |

### 教材系

#### 教材(text)→idにより対象の教材管理

| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL |  |
| name | varchar | NO |  | NULL |  |
| thumbnail | image | NO |  | NULL |  |
| genre_id | int | NO | FOREIGN_KEY | NULL |  |

#### 教材ジャンル(genre)

| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL |  |
| name | varchar | NO |  | NULL |  |

#### 教材(動画)コメント(comment)

| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL |  |
| created_at |  | NO |  | NULL |  |
| comment | varchar | NO |  | NULL |  |
| text_id | int | NO | FOREIGN_KEY | NULL |  |
| user_id | int | NO | FOREIGN_KEY | NULL |  |

### チャット系(1onN)

#### 情報共有ルーム(info-room)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| room-name | varchar | NO |  | NULL |  |

#### 情報共有メッセージ(info_message)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| message | varchar | NO |  | NULL |  |
| user_id | int | NO | FOREIGN_KEY | NULL |  |
| info_room_id | int | NO | FOREIGN_KEY | NULL |  |

#### 質問スレッド(question_room)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| room-name | varchar | NO |  | NULL |  |

#### 質問メッセージ(question_message)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| message | varchar | NO |  | NULL |  |
| user_id | int | NO | FOREIGN_KEY | NULL |  |
| question_room_id | int | NO | FOREIGN_KEY | NULL |  |

### チャット系(1on1)

#### 学生と企業のチャットルーム(scout_room)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| user_id | int | NO | FOREIGN_KEY | NULL |  |
| company_id | int | NO | FOREIGN_KEY | NULL |  |

#### 学生と企業間のメッセージ(scout_message)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| scout_room_id | int | NO | FOREIGN_KEY | NULL |  |
| user_id | int | YES | FOREIGN_KEY | NULL |  |
| company_id | int | YES | FOREIGN_KEY | NULL |  |

#### 1on1のチャットルーム(riwb_room)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| user_id | int | NO | FOREIGN_KEY | NULL | students(staff=False) |
| user_id | int | NO | FOREIGN_KEY | NULL | students(staff=True) |

#### 1on1のメッセージ(riwb_message)


| Field | Type | Null | Key | Default | Extra |
| :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | NO | PRI | NULL | auto-increm |
| created_at |  | NO |  | NULL |  |
| riwb_room_id | int | NO | FOREIGN_KEY | NULL |  |
| user_id | int | YES | FOREIGN_KEY | NULL |  |

## 議題

- 自己分析のテーブルや内容  
- 情報共有のチャット形態  
- コメントに対するリプやコメント、作るのか、作り方  
- 教材の内容について、今後AI,WEB以外の教材を配信し、動画以外の教材も作るのか  