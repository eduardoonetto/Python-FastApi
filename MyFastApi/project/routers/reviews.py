from ..common import get_current_user
from ..schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel
from fastapi import APIRouter, Depends, HTTPException
from ..database import User, Movie, UserReview
from typing import List

router = APIRouter(prefix='/reviews')

@router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel, user: User = Depends(get_current_user)):

  
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='Movie Not Found')

    user_review = UserReview.create(
        user_id     = user.id,
        movie_id    = user_review.movie_id,
        review      = user_review.review,
        score       = user_review.score
    )

    return user_review

#get reviews
@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)
    return [user_review for user_review in reviews]

#get review by id
@router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    review = UserReview.select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    return review

#update review by id
@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel,  user: User = Depends(get_current_user)):
    
    query_review = UserReview.select().where(UserReview.id == review_id).first()
    
    if query_review.user_id != user.id:
        raise HTTPException(status_code=401, detail='No eres Propietario de esta review') 

    if query_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    query_review.review = review_request.review
    query_review.score = review_request.score
    query_review.save()

    return query_review

#delete review by id
@router.delete('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int,  user: User = Depends(get_current_user)):
    
    query_review = UserReview.select().where(UserReview.id == review_id).first()

    if query_review.user_id != user.id:
        raise HTTPException(status_code=404, detail='No eres el propietario')

    if query_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')
    
    query_review.delete_instance()
    return query_review