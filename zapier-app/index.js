const authentication = require('./authentication');
const newRoomTrigger = require('./triggers/newRoom');
const newReviewTrigger = require('./triggers/newReview');
const createRoomAction = require('./creates/createRoom');
const createReviewAction = require('./creates/createReview');
const searchMoviesAction = require('./searches/searchMovies');

module.exports = {
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,
  authentication,
  triggers: {
    [newRoomTrigger.key]: newRoomTrigger,
    [newReviewTrigger.key]: newReviewTrigger,
  },
  creates: {
    [createRoomAction.key]: createRoomAction,
    [createReviewAction.key]: createReviewAction,
  },
  searches: {
    [searchMoviesAction.key]: searchMoviesAction,
  },
};



