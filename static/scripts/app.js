var PostsBox = React.createClass({
  getInitialState: function() {
    return {posts: []};
  },

  loadPosts: function() {
    $.ajax({
      url: '/posts',
      dataType: 'json',
      cache: false,
      success: function(result) {
        this.setState({posts: result.posts});
      }.bind(this)
    });
  },

  componentDidMount: function() {
    this.loadPosts();
    setInterval(this.loadPosts, this.props.pollInterval);
  },

  handlePostSubmit: function(title, content) {
    $.ajax({
      url: '/posts',
      dataType: 'json',
      type: 'POST',
      data: { title: title, content: content },
      success: function(result) {
        this.setState({posts: result.posts});
      }.bind(this)
    });
  },

  handlePostDelete: function(post_id) {
    $.ajax({
      url: '/posts/' + post_id,
      dataType: 'json',
      type: 'DELETE',
      success: function(result) {
        this.setState({posts: result.posts});
      }.bind(this)
    });
  },

  render: function() {
    return (
      <div className="postsBox" >
        <h1>React Blog</h1>
        <NewPostForm onPostSubmit={this.handlePostSubmit} />
        <PostsList posts={this.state.posts} onPostDelete={this.handlePostDelete}/>
      </div>
    );
  }
});

var NewPostForm = React.createClass({
  getInitialState: function() {
    return { title: '', content: '' };
  },

  handleFormSubmit: function(e) {
    e.preventDefault();
    this.props.onPostSubmit(this.state.title, this.state.content);
    this.setState({ title: '', content: '' });
  },

  handleTitleChange: function(e) {
    this.setState({title: e.target.value});
  },

  handleContentChange: function(e) {
    this.setState({content: e.target.value});
  },

  render: function() {
    return (
      <div className="newPostBox">
        <h2>New post</h2>
        <form className="newPostForm" onSubmit={this.handleFormSubmit}>
          <input
            type="text"
            placeholder="Post title"
            value={this.state.title}
            onChange={this.handleTitleChange} />
          <textarea onChange={this.handleContentChange} value={this.state.content}></textarea>
          <PreviewArea content={this.state.content} />
          <div className="clear" />
          <input type="submit" value="Save" />
        </form>
      </div>
    );
  }
});

var PreviewArea = React.createClass({
  rawMarkup: function() {
    var rawMarkup = marked(this.props.content.toString(), {sanitize: true});
    return { __html: rawMarkup };
  },

  render: function() {
    return(
      <div className="postContentPreview">
        <h4>Preview</h4>
        <span dangerouslySetInnerHTML={this.rawMarkup()} />
      </div>
    );
  }
});

var PostsList = React.createClass({
  render: function() {
    var postsNodes = this.props.posts.map(function(post) {
      return (
        <div key={post.id} className="postsList">
          <Post id={post.id} title={post.title} content={post.content} pubDate={post.pub_date} onPostDelete={this.props.onPostDelete}/>
        </div>
      );
    }.bind(this));
    return (
      <div className="postsList">
        {postsNodes}
      </div>
    );
  }
});

var Post = React.createClass({
  rawMarkup: function() {
    var rawMarkup = marked(this.props.content.toString(), {sanitize: true});
    return { __html: rawMarkup };
  },

  handlePostDelete: function(e) {
    e.preventDefault();
    this.props.onPostDelete(this.props.id);
  },

  render: function() {
    return(
      <div className="post">
        <h2 className="postTitle">{this.props.title} <a href="#" onClick={this.handlePostDelete}>x</a></h2>
        <div className="postContent">
          <span dangerouslySetInnerHTML={this.rawMarkup()} />
        </div>
        <div className="postPubDate">
          <small>{this.props.pubDate}</small>
        </div>
      </div>
    );
  }
});

ReactDOM.render(
  <PostsBox pollInterval={5000} /> ,
  document.getElementById('content')
);
