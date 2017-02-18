<?xml version="1.0" encoding="utf-8"?>
<extension version="2.5" type="template" client="site">
    <name>{name}</name>
    <creationDate>{creationDate}</creationDate>
    <author>{author}</author>
    <authorEmail>{authorEmail}</authorEmail>
    <authorUrl>{authorUrl}</authorUrl>
    <copyright>{copyright}</copyright>
    <license>{license}</license>
    <version>{version}</version>
    <description>TPL_WHITESQUARE_XML_DESCRIPTION</description>

    <files>
        <folder>css</folder>
        <folder>images</folder>
        <folder>js</folder>
        <folder>language</folder>
        <filename>component.php</filename>
        <filename>error.php</filename>
        <filename>index.php</filename>
        <filename>templateDetails.xml</filename>
    </files>

    <positions>
    </positions>

    <languages folder="language">
        <language tag="{language}">{language}/{language}.tpl_{name}.ini</language>
        <language tag="{language}">{language}/{language}.tpl_{name}.sys.ini</language>
    </languages>
</extension>