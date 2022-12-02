// コメントのオンオフボタン
let comment_btn = document.getElementById('comment-btn');
// コメントのフォーム
let comment_box = document.getElementById('comment-input');

//styleのdisplay(表示非表示)を変更する関数、変更後がコメント仕様
let changeCommentElement = (el)=> {

  if(el.style.display=='flex'){
    el.style.display='none';
  }else{
    el.style.display='flex';
  }

}

//コメントフォーム関数をボタンクリック時に実行
comment_btn.addEventListener('click', ()=> {
  changeCommentElement(comment_box);
}, false);