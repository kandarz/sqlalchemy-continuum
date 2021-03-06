from tests import TestCase


class TestTableBuilder(TestCase):
    def test_assigns_foreign_keys_for_versions(self):
        article = self.Article()
        article.name = u'Some article'
        article.content = u'Some content'
        article.tags.append(self.Tag(name=u'some tag'))
        self.session.add(article)
        self.session.commit()
        cls = self.Tag.__versioned__['class']
        version = self.session.query(cls).first()
        assert version.name == u'some tag'
        assert version.id == 1
        assert version.article_id == 1

    def test_versioned_table_structure(self):
        table = self.Article.__versioned__['class'].__table__
        assert 'id' in table.c
        assert 'name' in table.c
        assert 'content' in table.c
        assert 'description'in table.c
        assert 'transaction_id' in table.c
        assert 'operation_type' in table.c

    def test_removes_autoincrementation(self):
        table = self.Article.__versioned__['class'].__table__
        assert table.c.id.autoincrement is False

    def test_removes_not_null_constraints(self):
        assert self.Article.__table__.c.name.nullable is False
        table = self.Article.__versioned__['class'].__table__
        assert table.c.name.nullable is True

    def test_primary_keys_remain_not_nullable(self):
        assert self.Article.__table__.c.name.nullable is False
        table = self.Article.__versioned__['class'].__table__
        assert table.c.id.nullable is False

    def test_transaction_id_column_not_nullable(self):
        assert self.Article.__table__.c.name.nullable is False
        table = self.Article.__versioned__['class'].__table__
        assert table.c.transaction_id.nullable is False
