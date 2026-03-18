def test_pdf_loader_returns_list():
    result = load_document("samples/test.pdf")
    assert isinstance(result, list)
    assert len(result) > 0