import { Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { HomePage } from './pages/HomePage';
import { GrammarLevelPage } from './pages/GrammarLevelPage';
import { GrammarLessonPage } from './pages/GrammarLessonPage';
import { VocabularyLevelPage } from './pages/VocabularyLevelPage';
import { QuizLevelPage } from './pages/QuizLevelPage';
import { BlogListPage } from './pages/BlogListPage';
import { BlogPostPage } from './pages/BlogPostPage';
import { NotFoundPage } from './pages/NotFoundPage';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="grammar/:level" element={<GrammarLevelPage />} />
        <Route path="grammar/:level/:lessonNumber" element={<GrammarLessonPage />} />
        <Route path="grammar/:level/:lessonNumber/:pointNumber" element={<GrammarLessonPage />} />
        <Route path="vocabulary/:level" element={<VocabularyLevelPage />} />
        <Route path="quiz/:level" element={<QuizLevelPage />} />
        <Route path="blog" element={<BlogListPage />} />
        <Route path="blog/:slug" element={<BlogPostPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
