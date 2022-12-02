import matplotlib.pyplot as plt

def enneagram(ans_lis):
  "エニアグラムの回答結果をリストで受け取り、棒グラフを画像にして返す関数"
  location = ['タイプ1', 'タイプ2', 'タイプ3', 'タイプ4', 'タイプ5', 'タイプ6', 'タイプ7', 'タイプ8', 'タイプ9']

  plt.bar(location,ans_lis)
  img = plt.savefig('result.png')
  return img

