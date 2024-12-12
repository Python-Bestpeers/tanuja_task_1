const toggleButton = document.getElementById('toggle-comment-form');
const commentForm = document.querySelector('.comment-form');

toggleButton.addEventListener('click', () => {
  commentForm.style.display = commentForm.style.display === 'none' || commentForm.style.display === '' ? 'block' : 'none';
});