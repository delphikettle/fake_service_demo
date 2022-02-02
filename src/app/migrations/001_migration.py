import peewee as pw

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Task(pw.Model):
        id = pw.UUIDField(primary_key=True)
        name = pw.TextField(unique=True, null=False)
        processing_time = pw.IntegerField(null=False)
        status = pw.IntegerField(null=False, default=1)

        class Meta:
            table_name = 'task'


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('task')
