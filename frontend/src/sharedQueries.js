import gql from "graphql-tag";

export const LOG_USER_IN = gql`
  mutation logUserIn($token: String!) {
    logUserIn(token: $token) @client
  }
`;

export const LOG_USER_OUT = gql`
  mutation logUserOut {
    logUserOut @client
  }
`;

export const USER_FRAGMENT = gql`
  fragment UserParts on UserType {
    id
    username
    profile {
      isFollowing
      avatar
    }
  }
`;

export const IMAGE_FRAGMENT = gql`
  fragment ImageParts on ImageType {
    id
    likeCount
    commentCount
    files {
      id
      url
    }
  }
`;

export const DETAIL_IMAGE_FRAGMENT = gql`
  fragment DetailParts on ImageType {
    id
    files {
      id
      url
    }
    caption
    location
    likeCount
    commentCount
    isLiked
    createdAt
    comments {
      id
      message
      creator {
        username
      }
    }
    creator {
      username
      profile {
        avatar
      }
    }
  }
`;
