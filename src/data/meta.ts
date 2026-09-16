import type { Level, Section } from './types';

export const LEVELS: Level[] = ['n1', 'n2', 'n3', 'n4', 'n5'];
export const SECTIONS: Section[] = ['grammar', 'vocabulary', 'quiz'];

export const SECTION_LABELS: Record<Section, string> = {
  grammar: '文法',
  vocabulary: '單字',
  quiz: '練習題',
};

export const LEVEL_LABELS: Record<Level, string> = {
  n1: 'N1',
  n2: 'N2',
  n3: 'N3',
  n4: 'N4',
  n5: 'N5',
};

export const SITE_NAME = '日檢手帖';
export const SITE_NAME_EN = 'NIKKEN TECHO';
export const SITE_TAGLINE = '像翻雜誌一樣，把日檢讀完。';
export const BLOG_LABEL = '部落格';

export function isLevel(value: string | undefined): value is Level {
  return LEVELS.includes(value as Level);
}

export function isSection(value: string | undefined): value is Section {
  return SECTIONS.includes(value as Section);
}
