FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --no-create-home appuser
COPY --chown=appuser:appuser src/ ./src/
USER 10001:10001
EXPOSE 8000
CMD ["python", "-m", "src.server"]
