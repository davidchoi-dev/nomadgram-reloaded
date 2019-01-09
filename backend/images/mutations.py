import graphene
from django.db import IntegrityError
from . import models, types


class LikeImage(graphene.Mutation):

    """ Like an Image """

    class Arguments:
        imageId = graphene.Int(required=True)

    Output = types.LikePhotoResponse

    def mutate(self, info, **kwargs):
        imageId = kwargs.get('imageId')
        user = info.context.user
        ok = True
        error = None
        if user.is_authenticated:
            try:
                image = models.Image.objects.get(id=imageId)
            except models.Image.DoesNotExist:
                ok = False
                error = 'Image Not Found'
                return types.LikePhotoResponse(ok=ok, error=error)

            try:
                like = models.Like.objects.get(
                    creator=user, image=image)
                like.delete()
                return types.LikePhotoResponse(ok=ok, error=error)
            except models.Like.DoesNotExist:
                pass

            try:
                like = models.Like.objects.create(
                    creator=user, image=image)
                like.save()
                return types.LikePhotoResponse(ok=ok, error=error)
            except IntegrityError:
                ok = False
                error = "Can't Like Photo"
                return types.LikePhotoResponse(ok=ok, error=error)
        else:
            ok = False
            error = 'You need to log in'
            return types.LikePhotoResponse(ok=ok, error=error)


class AddComment(graphene.Mutation):

    """ Add Comment """

    class Arguments:
        imageId = graphene.Int(required=True)
        message = graphene.String(required=True)

    Output = types.AddCommentResponse

    def mutate(self, info, **kwargs):
        imageId = kwargs.get('imageId')
        message = kwargs.get('message')

        user = info.context.user

        ok = True
        error = None
        comment = None

        if user.is_authenticated:
            try:
                image = models.Image.objects.get(id=imageId)
            except models.Image.DoesNotExist:
                ok = False
                error = 'Image Not Found'
                return types.AddCommentResponse(ok=ok, error=error, comment=comment)

            try:
                comment = models.Comment.objects.create(
                    message=message, image=image, creator=user)
                return types.AddCommentResponse(ok=ok, error=error, comment=comment)
            except IntegrityError:
                ok = False
                error = "Can't create the comment"
                return types.AddCommentResponse(ok=ok, error=error, comment=comment)
        else:
            ok = False
            error = 'You need to log in'
            return types.AddCommentResponse(ok=ok, error=error, comment=comment)


class DeleteComment(graphene.Mutation):

    class Arguments:
        imageId = graphene.Int(required=True)
        commentId = graphene.Int(required=True)

    Output = types.DeleteCommentResponse

    def mutate(self, info, **kwargs):
        imageId = kwargs.get('imageId')
        commentId = kwargs.get('commentId')

        user = info.context.user

        ok = True
        error = None

        if user.is_authenticated:

            try:
                image = models.Image.objects.get(id=imageId)
            except models.Image.DoesNotExist:
                ok = False
                error = 'Image Not Found'
                return types.DeleteCommentResponse(ok=ok, error=error)

            try:
                comment = models.Comment.objects.get(id=commentId)
            except models.Comment.DoesNotExist:
                ok = False
                error = 'Comment Not Found'
                return types.DeleteCommentResponse(ok=ok, error=error)

            if comment.creator.id == user.id or image.creator.id == user.id:
                comment.delete()
            else:
                ok = False
                error = "Can't Delete Comment"
            return types.DeleteCommentResponse(ok=ok, error=error)

        else:
            ok = False
            error = 'You need to log in'
            return types.DeleteCommentResponse(ok=ok, error=error)
