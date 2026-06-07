import { useState } from "react";

function NewsCard({ article, index }) {

  const [level, setLevel] = useState("beginner");

  const [slides, setSlides] = useState(
    article.slides || null
  );

  const [currentSlide, setCurrentSlide] =
    useState(0);

  const [loadingSlides, setLoadingSlides] =
    useState(false);

  const [liked, setLiked] =
    useState(false);

  const [likeCount, setLikeCount] =
    useState(32);

  const [saved, setSaved] =
    useState(false);

  const [showComments, setShowComments] =
    useState(false);

  const [commentText, setCommentText] =
    useState("");

  const [comments, setComments] =
    useState([]);

  const [showBot, setShowBot] =
    useState(false);

  const [botInput, setBotInput] =
    useState("");

  const [chatMessages, setChatMessages] =
    useState([
      {
        type: "ai",
        text:
          "Hey! I've read the article. Ask me anything."
      }
    ]);

  const currentSlides =
    slides?.[level] || [];

  async function generateSlides() {

    if (slides) return;

    if (loadingSlides) return;

    try {

      setLoadingSlides(true);

      const response = await fetch(
        "http://127.0.0.1:5000/generate-slides",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            title: article.title,
            desc: article.desc,
            content:
              article.content || "",
            index
          })
        }
      );

      const data =
        await response.json();

      setSlides(data.slides);

    } catch (err) {

      console.error(
        "Slide generation failed",
        err
      );

    } finally {

      setLoadingSlides(false);

    }
  }

  function toggleLike() {

    if (liked) {

      setLiked(false);

      setLikeCount(prev => prev - 1);

    } else {

      setLiked(true);

      setLikeCount(prev => prev + 1);

    }
  }

  function toggleSave() {

    const key =
      "savedArticles";

    const item = {
      id: index,
      title: article.title,
      desc: article.desc,
      image: article.image,
      domain: article.domain
    };

    let savedArticles =
      JSON.parse(
        localStorage.getItem(key) ||
        "[]"
      );

    if (!saved) {

      savedArticles.push(item);

      setSaved(true);

    } else {

      savedArticles =
        savedArticles.filter(
          x => x.id !== index
        );

      setSaved(false);
    }

    localStorage.setItem(
      key,
      JSON.stringify(savedArticles)
    );
  }

  function addComment() {

    if (!commentText.trim())
      return;

    setComments(prev => [
      ...prev,
      commentText
    ]);

    setCommentText("");
  }

  async function sendArticleChat() {

    if (!botInput.trim())
      return;

    const userText =
      botInput;

    setChatMessages(prev => [
      ...prev,
      {
        type: "user",
        text: userText
      }
    ]);

    setBotInput("");

    try {

      const response =
        await fetch(
          "http://127.0.0.1:5000/ask-article",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
              question:
                userText,

              article: `
              Title:
              ${article.title}

              Description:
              ${article.desc}
              `
            })
          }
        );

      const data =
        await response.json();

      setChatMessages(prev => [
        ...prev,
        {
          type: "ai",
          text: data.reply
        }
      ]);

    } catch {

      setChatMessages(prev => [
        ...prev,
        {
          type: "ai",
          text:
            "AI unavailable."
        }
      ]);
    }
  }

  return (

    <div className="news-card">

      <div className="card-image">

        <img
          src={article.image}
          alt=""
        />

        <span className="domain-pill">
          {article.domain}
        </span>

        <div
          className={`save-btn ${
            saved
              ? "saved"
              : ""
          }`}
          onClick={toggleSave}
        >
          <img
            src="/images/save.svg"
            alt=""
          />
        </div>

      </div>

      <div className="card-content">

        <div className="cardContent">

          <h2 className="card-title">

            {
              currentSlides[
                currentSlide
              ]?.title ||
              article.title
            }

          </h2>

          <p className="card-desc">

            {
              currentSlides[
                currentSlide
              ]?.desc ||
              article.desc
            }

          </p>

        </div>

        <button
          className="next-btn"
          onClick={async () => {

            if (!slides) {

              await generateSlides();

              return;
            }

            setCurrentSlide(
              prev =>
                (prev + 1) %
                currentSlides.length
            );
          }}
        >
          <img
            src="/images/arrow-right.png"
            alt=""
          />
        </button>

        <div className="card-actions">

          <div className="left-actions">

            <div
              className={`action like-action ${
                liked
                  ? "liked"
                  : ""
              }`}
              onClick={toggleLike}
            >

<img
  src={
    liked
      ? "/images/like-filled.png"
      : "/images/like.png"
  }
  className="like-icon"
  alt=""
/>

              <span className="like-count">
                {likeCount}
              </span>

            </div>

            <div
              className="action comment-action"
              onClick={() =>
                setShowComments(
                  !showComments
                )
              }
            >

              <img
                src="/images/comment.svg"
                alt=""
              />

              <span className="comment-count">
                {comments.length}
              </span>

            </div>

            <div
              className="action"
              onClick={() =>
                navigator.share?.({
                  title:
                    article.title,
                  text:
                    article.desc
                })
              }
            >
              <img
                src="/images/share.svg"
                alt=""
              />
              <span>
                Share
              </span>
            </div>

            <div className="level-toggle">

              {[
                "beginner",
                "intermediate",
                "advanced"
              ].map(item => (

                <button
                  key={item}
                  className={`level-btn ${
                    level === item
                      ? "active"
                      : ""
                  }`}
                  onClick={async () => {

                    if (!slides)
                      await generateSlides();

                    setLevel(item);

                    setCurrentSlide(
                      0
                    );
                  }}
                >
                  {item[0]
                    .toUpperCase()}
                </button>

              ))}

            </div>

          </div>

          <button
            className={`chatbot-btn ${
              showBot
                ? "active"
                : ""
            }`}
            onClick={() =>
              setShowBot(
                !showBot
              )
            }
          >

            <img
              src="/images/bot.svg"
              alt=""
            />

            <span>
              Ask Bot
            </span>

          </button>

        </div>

        {showComments && (

          <div className="comment-section show">

            <div className="comments-list">

              {comments.map(
                (comment, i) => (

                  <div
                    className="comment-item"
                    key={i}
                  >

                    <div className="comment-avatar">
                      Y
                    </div>

                    <div className="comment-content">

                      <div className="comment-header">
                        <strong>
                          You
                        </strong>
                      </div>

                      <div className="comment-text">
                        {comment}
                      </div>

                    </div>

                  </div>
                )
              )}

            </div>

            <div className="comment-input-box">

              <input
                value={
                  commentText
                }
                onChange={e =>
                  setCommentText(
                    e.target.value
                  )
                }
                placeholder="Write a comment..."
              />

              <button
                onClick={
                  addComment
                }
              >
                <img
                  src="/images/send.png"
                  alt=""
                />
              </button>

            </div>

          </div>
        )}

        {showBot && (

          <div className="article-bot show">

            <div className="bot-header">

              <div className="bot-title">

                <img
                  src="/images/bot-white.png"
                  alt=""
                />

                <span>
                  Article Bot
                </span>

              </div>

            </div>

            <div className="bot-body">

              <div className="bot-chat">

                {chatMessages.map(
                  (
                    msg,
                    i
                  ) => (

                    <div
                      key={i}
                      className={`msg ${msg.type}`}
                    >
                      {msg.text}
                    </div>
                  )
                )}

              </div>

              <div className="bot-input">

                <input
                  value={
                    botInput
                  }
                  onChange={e =>
                    setBotInput(
                      e.target.value
                    )
                  }
                  placeholder="Ask about this article..."
                />

                <button
                  onClick={
                    sendArticleChat
                  }
                >
                  <img
                    src="/images/send.png"
                    alt=""
                  />
                </button>

              </div>

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default NewsCard;