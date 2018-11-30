from ..nodes import Media


def like(self):

    self.logger.info('medias: {}'.format(self._acc))

    for media in self._acc:
        if isinstance(media, Media):
            id = media.id
        else:
            url = media
            id = Media.get_media_id_from_link(url)
            self.logger.info('id: {}'.format(id))

        if self._api.like(id):
            self.logger.info('liked media %d.' % id)
        else:
            self.logger.error('can\'t like')

    self._reset()
